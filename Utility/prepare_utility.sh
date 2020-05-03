#!/bin/bash
BR_NAME=buildroot-2020.02
BR_FILE=${BR_NAME}.tar.bz2
BR_DL=../${BR_FILE}
set -e
if [ ! -f ${BR_DL} ] || ! (bzip2 -q -t ${BR_DL}); then
  (
    cd ..
    rm -f ${BR_FILE}
    wget https://buildroot.org/downloads/${BR_FILE}
  )
fi
tar -xjf ${BR_DL}
cp BR_config ${BR_NAME}/.config
cd buildroot-2020.02
for i in ../patches/*; do
  patch -p1 <$i
done
make

set -e
SRC_DIR=buildroot-2020.02/output/images
DST_DIR=../Admin/user_img
cp -L ${SRC_DIR}/rootfs.ext4 ${DST_DIR}/rootfs.ext4
cp ${SRC_DIR}/zImage ${DST_DIR}/zImage_user
cp ${SRC_DIR}/vexpress-v2p-ca9.dtb ${DST_DIR}/vexpress-v2p-ca9-user.dtb
