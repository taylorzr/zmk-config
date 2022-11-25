# zmk

## setup

```sh
pip3 install --user -U west
brew install --cask gcc-arm-embedded
west init -l app/
west update
west zephyr-export
pip3 install --user -r zephyr/scripts/requirements-base.txt
source zephyr/zephyr-env.sh
```

## build/flash

```sh
cd app
source zephyr/zephyr-env.sh
export ZEPHYR_TOOLCHAIN_VARIANT=gnuarmemb GNUARMEMB_TOOLCHAIN_PATH=/Applications/ArmGNUToolchain/12.2.mpacbti-bet1/arm-none-eabi
west build -d build_chonk_left -b nice_nano_v2 -- -DSHIELD=lil_chonky_bois_left -DZMK_CONFIG="$HOME/code/zmk-config/config"
sleep 8 && cp build_chonk_left/zephyr/zmk.uf2 /run/media/taylorzr/NICENANO/
# and reset controller while sleeping
```
