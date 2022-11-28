.PHONY: dux fdux chonk fchonk

dux:
	cd ../zmk/app && west build --pristine -d build_a_dux_left -b nice_nano_v2 -- -DSHIELD=a_dux_left -DZMK_CONFIG="${HOME}/code/zmk-config/config"

fdux:
	cd ../zmk/app && cp build_a_dux_left/zephyr/zmk.uf2 /run/media/taylorzr/NICENANO/

chonk:
	cd ../zmk/app && west build --pristine -d build_lil_chonky_bois_left -b nice_nano_v2 -- -DSHIELD=lil_chonky_bois_left -DZMK_CONFIG="${HOME}/code/zmk-config/config"

fchonk:
	cd ../zmk/app && cp build_lil_chonky_bois_left/zephyr/zmk.uf2 /run/media/taylorzr/NICENANO/
