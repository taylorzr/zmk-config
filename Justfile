default:
  just --list

dux mode="build" side="left":
  just {{mode}} a_dux_{{side}} nice_nano_v2 NICENANO

chonk mode="build" side="left":
  just {{mode}} lil_chonky_bois_{{side}} nice_nano_v2 NICENANO

goshawk mode="build":
  just {{mode}} goshawk nice_nano_v2 NICENANO

banana mode="build":
	just {{mode}} banana seeeduino_xiao_ble XIAO-SENSE

xiao mode="build":
	just {{mode}} tester_xiao seeeduino_xiao_ble XIAO-SENSE
	# cd ../zmk/app && west build --pristine -d build_xiao -b seeeduino_xiao_ble -- -DSHIELD=tester_xiao

osprette mode="build":
  just {{mode}} osprette nice_nano_v2 NICENANO

tern mode="build":
  just {{mode}} tern_ble seeeduino_xiao_ble XIAO-SENSE

[private]
alias b := build

[private]
build shield microcontroller drive:
	cd ../zmk/app && west build --pristine -d build_{{shield}} -b {{microcontroller}} -- -DSHIELD={{shield}} -DZMK_CONFIG="${HOME}/code/zmk-config/config" -DZMK_EXTRA_MODULES="${HOME}/code/zmk-auto-layer"

[private]
alias f := flash

[private]
flash shield microcontroller drive:
  sleep 10
  cp ../zmk/app/build_{{shield}}/zephyr/zmk.uf2 /run/media/{{env('USER')}}/{{drive}}/

init: deps zephyr zmk

deps:
  sudo dnf group install development-tools  # new name ? "C Development Tools and Libraries"
  sudo dnf install git cmake ninja-build gperf ccache dfu-util dtc wget python3-pip python3-tkinter xz file glibc-devel.i686 libstdc++-devel.i686 python38  SDL2-devel
 
zephyr version="0.16.3":
  # wget https://github.com/zephyrproject-rtos/sdk-ng/releases/download/v{{version}}/zephyr-sdk-{{version}}_linux-x86_64.tar.xz
  # wget -O - https://github.com/zephyrproject-rtos/sdk-ng/releases/download/v{{version}}/sha256.sum | shasum --check --ignore-missing
  tar xvf zephyr-sdk-{{version}}_linux-x86_64.tar.xz
  rm zephyr-sdk-{{version}}_linux-x86_64.tar.xz
  cd zephyr-sdk-{{version}} && ./setup.sh
 
# see https://zmk.dev/docs/development/local-toolchain/setup/native
[working-directory: '../zmk']
zmk:
  pipx install -U west
  west init -l app/
  west update
  west zephyr-export
  python -m venv .venv
  source .venv/bin/activate
  pip install -r zephyr/scripts/requirements.txt
  # source $(HOME)/.local/zephyr-sdk-0.15.0/environment-setup-x86_64-pokysdk-linux
  # TODO: maybe need to do this somewhere?
 
