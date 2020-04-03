#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>
#include <gpiod.h>

// Documentation
// https://github.com/brgl/libgpiod/blob/master/include/gpiod.h

// Catch SIGINT to notify game end and properly close open devices
int LAST_SIGNAL;
void sig_handler(int sig)
{
  LAST_SIGNAL = sig;
}

void safe_fail(struct gpiod_chip *chip, const char *fmessage)
{
  gpiod_chip_close(chip);
  fprintf(stderr, fmessage);
  exit(EXIT_FAILURE);
}

int main(int argc, char *argv[])
{
  // Setup SIGINT catch
  if (signal(SIGINT, sig_handler) == SIG_ERR)
    fprintf(stderr, "Couldn't setup signal handler.\n");

  // Open chip
  struct gpiod_chip *chip;
  if ((chip = gpiod_chip_open("/dev/gpiochip1")) == NULL)
    safe_fail(chip, "[error] Chip open failed.");
  fprintf(stderr, "Initialized chip.\n");

  // Initialize game and loop variables
  int is_value_set = 0;
  int game_value = 0;
  int player_value = 0;
  int score = 0;

  int loop_value;
  int i;
  int multiplier = 1;

  fprintf(stderr, "Initializing chip line connections.\n");

  // Initialize and request Led Lines in bulk
  fprintf(stderr, "Creating led bulk.\n");
  struct gpiod_line_bulk led_bulk;
  unsigned int led_offsets[8] = {24, 25, 26, 27, 28, 29, 30, 31};
  if (gpiod_chip_get_lines(chip, led_offsets, 8, &led_bulk) < 0)
    safe_fail(chip, "[error] Led bulk failed.\n");
  if (gpiod_line_request_bulk_output(&led_bulk, "led", 0) < 0)
    safe_fail(chip, "Led request failed.\n");
  const int led_off[8] = {0, 0, 0, 0, 0, 0, 0, 0};
  const int led_on[8] = {1, 1, 1, 1, 1, 1, 1, 1};
  int led_setup[8] = {0, 0, 0, 0, 0, 0, 0, 0};

  // Initialize and request Button Lines in bulk
  fprintf(stderr, "Creating button bulk.\n");
  struct gpiod_line_bulk button_bulk;
  unsigned int button_offsets[12] = {12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23};
  if (gpiod_chip_get_lines(chip, button_offsets, 12, &button_bulk) < 0)
    safe_fail(chip, "Button bulk failed.\n");
  if (gpiod_line_request_bulk_falling_edge_events(&button_bulk, "button") < 0)
    safe_fail(chip, "Button request failed.\n");

  // Initialize and request Switch Lines in bulk
  fprintf(stderr, "Creating switch bulk.\n");
  struct gpiod_line_bulk switch_bulk;
  unsigned int switch_offsets[12] = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11};
  if (gpiod_chip_get_lines(chip, switch_offsets, 12, &switch_bulk) < 0)
    safe_fail(chip, "Switch bulk failed.\n");
  if (gpiod_line_request_bulk_both_edges_events(&switch_bulk, "switch") < 0)
    safe_fail(chip, "Switch request failed.\n");

  // Timespecs setup
  const struct timespec timeout = {2, 0};
  struct timespec last_event_ts;

  // Initialize event variables
  int event_line_offset;
  int wait_result = 0;
  int switch_value;
  struct gpiod_line_event last_event;
  struct gpiod_line_bulk event_bulk;

  fprintf(stderr, "Initialized game variables.\n");

  // Begin game
  printf("Beginning math game application.\n");
  printf("Welcome to the Math Game\nUse the buttons to add numbers to a sum equal to the sum of led values.\nUse switches to indicate addition or subtraction.\n");
  sleep(3);

  // Game loop
  while (true)
  {
    // Game value setup
    if (!is_value_set)
    {
      // Choose at random on each iteration if a led should be on or off
      // if on, then add that value to total sum
      for (i = 24; i < 32; i++)
      {
        multiplier = rand() % 2;
        led_setup[i - 24] = multiplier;
        loop_value = multiplier * i;

        game_value += loop_value;
      }
      // Use array of boolean ints to set led states
      if (gpiod_line_set_value_bulk(&led_bulk, led_setup) < 0)
        safe_fail(chip, "Led set failed.\n");

      printf("Game value set to [ %i ]\n", game_value);
      is_value_set = 1;
    }

    // Initial do while loop for waiting on user button press
    do
    {
      wait_result = gpiod_line_event_wait_bulk(&button_bulk, &timeout, &event_bulk);
      fprintf(stderr, "Waiting for user to click a button... [%i]\n", wait_result);
      if (wait_result < 0 || LAST_SIGNAL == SIGINT)
        break;
    } while (wait_result <= 0);

    // Helper do while loop to counteract against bouncing
    do
    {
      if (wait_result < 0 || LAST_SIGNAL == SIGINT)
        break;

      // Clear last event from buffer - required to not trigger event_wait on next game loop
      // Also helps to remove oscillations caused by bouncing effect
      if (gpiod_line_event_read(event_bulk.lines[0], &last_event) < 0)
        safe_fail(chip, "Event read failed.\n");

      wait_result = gpiod_line_event_wait(event_bulk.lines[0], &timeout);
      fprintf(stderr, "Cleared event buffer for event line. [%i]\n", wait_result);
    } while (wait_result == 1);

    if (LAST_SIGNAL == SIGINT)
      break;

    // Get the offset of the triggered button and the state of its respective switch
    event_line_offset = gpiod_line_offset(event_bulk.lines[0]);
    if ((switch_value = gpiod_line_get_value(switch_bulk.lines[event_line_offset - 12])) < 0)
      safe_fail(chip, "Event get line failed.\n");

    fprintf(stderr, "Event-triggered lines count: %i\n", event_bulk.num_lines);
    fprintf(stderr, "Event-triggered line offset: %i\n", event_line_offset);
    fprintf(stderr, "Event timestamp and type: %lld.%.9ld, %i\n", (long long)last_event.ts.tv_sec, last_event.ts.tv_nsec, last_event.event_type);
    fprintf(stderr, "Respective switch value: %i\n", switch_value);

    // Set multiplier based on switch state
    switch (switch_value)
    {
    case 0:
      multiplier = -1;
      break;
    case 1:
      multiplier = 1;
      break;
    }

    fprintf(stderr, "Multiplier value is: %i\n", multiplier);

    // Set player value
    player_value += multiplier * event_line_offset;
    printf("Player value: %i [+ (%i)] / %i\n", player_value, multiplier * event_line_offset, game_value);

    // Win condition
    if (player_value == game_value)
    {
      is_value_set = 0;
      player_value = 0;
      game_value = 0;

      score += 1;

      printf("Game finished, restarting...\n");

      // Flash led loop
      if (score > 0)
        for (i = 0; i < 3; i++)
        {
          if (gpiod_line_set_value_bulk(&led_bulk, led_on) < 0) safe_fail(chip, "Led set failed.\n");
          sleep(1);
          if (gpiod_line_set_value_bulk(&led_bulk, led_off) < 0) safe_fail(chip, "Led set failed.\n");
          sleep(1);
        }
    }
  }

  gpiod_chip_close(chip);
}
