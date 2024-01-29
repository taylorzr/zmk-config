.PHONY:
.ONESHELL:

setup: tools zephyr zmk

tools:
ifeq ($(UNAME), Linux)
	sudo dnf group install "Development Tools" "C Development Tools and Libraries"
	sudo dnf install git cmake ninja-build gperf ccache dfu-util dtc wget python3-pip python3-tkinter xz file glibc-devel.i686 libstdc++-devel.i686 python38  SDL2-devel
endif
ifeq ($(UNAME), Darwin)
endif

zephyr:
ifeq ($(UNAME), Linux)
	$(HOME)/.local/zephyr-sdk-0.15.0
endif
ifeq ($(UNAME), Darwin)
endif

$(HOME)/.local/zephyr-sdk-0.15.0:
ifeq ($(UNAME), Linux)
	cd $(HOME)/.local
	wget https://github.com/zephyrproject-rtos/sdk-ng/releases/download/v0.15.0/zephyr-sdk-0.15.0_linux-x86_64.tar.gz
	wget -O - https://github.com/zephyrproject-rtos/sdk-ng/releases/download/v0.15.0/sha256.sum | shasum --check --ignore-missing
	tar xvf zephyr-sdk-0.15.0_linux-x86_64.tar.gz
	rm zephyr-sdk-0.15.0_linux-x86_64.tar.gz
	cd zephyr-sdk-0.15.0
	./setup.sh
	pip3 install --user -U west
endif
ifeq ($(UNAME), Darwin)
endif

zmk:
	cd ../zmk
	west init -l app/
	west update
	west zephyr-export
	pip3 install --user -r zephyr/scripts/requirements.txt
	# TODO: maybe need to do this somewhere?
	# source $(HOME)/.local/zephyr-sdk-0.15.0/environment-setup-x86_64-pokysdk-linux

dux:
	cd ../zmk/app
	west build --pristine -d build_a_dux_left -b nice_nano_v2 -- -DSHIELD=a_dux_left -DZMK_CONFIG="${HOME}/code/zmk-config/config"

fdux:
	cd ../zmk/app
	cp build_a_dux_left/zephyr/zmk.uf2 /run/media/$(USER)/NICENANO/

chonk:
	cd ../zmk/app
	west build --pristine -d build_lil_chonky_bois_left -b nice_nano_v2 -- -DSHIELD=lil_chonky_bois_left -DZMK_CONFIG="${HOME}/code/zmk-config/config"

rchonk:
	cd ../zmk/app
	west build --pristine -d build_lil_chonky_bois_right -b nice_nano_v2 -- -DSHIELD=lil_chonky_bois_right -DZMK_CONFIG="${HOME}/code/zmk-config/config"

chonkf:
	cd ../zmk/app
	cp build_lil_chonky_bois_left/zephyr/zmk.uf2 /run/media/$(USER)/NICENANO/

rchonkf:
	cd ../zmk/app
	cp build_lil_chonky_bois_right/zephyr/zmk.uf2 /run/media/$(USER)/NICENANO/
