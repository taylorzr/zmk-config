#!/bin/bash
DIR="$( cd -P "$( dirname "$0" )" && pwd )"
# /Projects/Github/zmk/app/boards/shields/scottowing
ROOTDIR=$DIR/../../../../
APPDIR=$DIR/../../../
pushd "$ROOTDIR"
source zephyr/zephyr-env.sh
popd
pushd "$APPDIR"
west config build.dir-fmt "build-reset" && west build --pristine -b nice_nano_v2 -- -DSHIELD=settings_reset
west config build.dir-fmt "build-left" && west build --pristine -b nice_nano_v2 -- -DSHIELD=scottowing_left
west config build.dir-fmt "build-right" && west build --pristine -b nice_nano_v2 -- -DSHIELD=scottowing_right
popd
