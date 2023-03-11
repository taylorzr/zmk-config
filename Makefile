.PHONY:
.ONESHELL:

deps:
	sudo dnf group install "Development Tools" "C Development Tools and Libraries"
	sudo dnf install git cmake ninja-build gperf ccache dfu-util dtc wget python3-pip python3-tkinter xz file glibc-devel.i686 libstdc++-devel.i686 python38  SDL2-devel
	wget https://github.com/zephyrproject-rtos/sdk-ng/releases/download/v0.15.0/zephyr-sdk-0.15.0_linux-x86_64.tar.gz
	wget -O - https://github.com/zephyrproject-rtos/sdk-ng/releases/download/v0.15.0/sha256.sum | shasum --check --ignore-missing
	tar xvf zephyr-sdk-0.15.0_linux-x86_64.tar.gz
	cd zephyr-sdk-0.15.0
	./setup.sh
	cd ..
	rm -rf zephyr-sdk-0.15.0
	rm zephyr-sdk-0.15.0_linux-x86_64.tar.gz

setup:
	cd ../zmk
	west init -l app/
	west update
	west zephyr-export
	pip3 install --user -r zephyr/scripts/requirements.txt

dux:
	cd ../zmk/app
	# source ../zephyr/zephyr-env.sh
	west build --pristine -d build_a_dux_left -b nice_nano_v2 -- -DSHIELD=a_dux_left -DZMK_CONFIG="${HOME}/code/zmk-config/config"

fdux:
	cd ../zmk/app
	cp build_a_dux_left/zephyr/zmk.uf2 /run/media/taylorzr/NICENANO/

chonk:
	cd ../zmk/app
	west build --pristine -d build_lil_chonky_bois_left -b nice_nano_v2 -- -DSHIELD=lil_chonky_bois_left -DZMK_CONFIG="${HOME}/code/zmk-config/config"

fchonk:
	cd ../zmk/app
	cp build_lil_chonky_bois_left/zephyr/zmk.uf2 /run/media/taylorzr/NICENANO/
