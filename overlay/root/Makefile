CC=$(CROSS_COMPILE)gcc
OBJS := mod.o
mod: $(OBJS)
	$(CC) -o mod $(CFLAGS) $(LDFLAGS) $(OBJS) -l gpiod
$(OBJS) : %.o : %.c
	$(CC) -c $(CFLAGS) $< -o $@


