#!/usr/bin/env python
# coding:utf-8
# Author:  mozman
# Purpose: svg examples
# Created: 07.11.2010
# Copyright (C) 2010, Manfred Moitzi
# License: MIT License

import svgwrite
from svgwrite import cm, mm

columns = 5
split = True

# TODO: Flush out class
class Keymap:
    def __init__(self, keys=34, columns=10, split=True, layers=[]):
        self.keys = keys
        self.columns = columns
        self.split = split
        self.layers = layers

layers = [
    """
      3/q     w       f     p b j l u y '
      a       alt/r   cmd/s t g m n e i o
      z       x       c     d v k h , . /
      ctl/esc sft/bsp 1/spc 2/-
    """,
    """""", # for combos
    """
      !  @  #   $   %  ^ &   *   =   +
       | c← c↓  c↑  c→ ← ↓   ↑   →   ;
      ~  `  '_' "_" |  + (_) {_} [_] \\
      <tr> <tr> <held> <tr>
    """,
    """
      <held> bt_0 bt_1   bt_2   <tr>         <tr> <tr> <tr> <tr> <tr>
      <tr>   <tr>   bt_prv bt_nxt <tr>         <tr> <tr> <tr> <tr> <tr>
      <tr>   <tr>   <tr>     <tr>     bootloader <tr> <tr> <tr> <tr> <tr>
      <tr>   <tr>   <tr>     <tr>
    """,
]

combos = [
    [1, 2, "untab"],
    [2, 3, "tab"],
    [1, 3, "␡"],
    [2, 4, "▶️"],
    [6, 7, "save"],
    [7, 8, "-"],
    [5, 7, "⏭"],
    # [12, 23, "ss copy"],
    # [22, 13, "ss file"],
    [21, 22, "copy"],
    [22, 23, "paste"],
    [21, 23, "cut"],
    [26, 27, "enter"],
    [27, 28, "_"],
    [16, 17, ":"],
    [17, 18, ";"],
    [11, 12, "c s ←"],
    [12, 13, "c s →"],
]

y_offsets = [10, 5, 0, 5, 5, 5, 5, 0, 5, 10]

spacing = 19
key_size = 18
maybe_center = 1
keycount = 34


def are_neighbors(k1, k2, columns):
    return k2 - k1 == 1 and k2 % columns != 0


def keymap(name):
    dwg = svgwrite.Drawing(filename=name, debug=True)
    for k, layer in enumerate(layers):
        keys = layer.split()

        positions = []

        for i in range(keycount):
            row, col = divmod(i, 10)

            # todo: handle thumb row better
            if i >= 30:
                col += 3

            x = 10 + (col * spacing)
            y = 10 + (k * 85) + (row * spacing) + y_offsets[col]

            if col >= 5:
                x += 15

            label = ""
            fill = "lightgray"

            if k != 1:
                label = keys[i]

                if label == "<held>":
                    fill = "khaki"
                    label = ""

                if label == "<tr>":
                    label = "▽"

            # todo: can't just enter newlines, have to do something fancier
            # if "|" in label and len(label) > 1:
            #     label = label.replace("|", "\n")

            dwg.add(
                dwg.rect(
                    insert=(x * mm, y * mm),
                    size=(key_size * mm, key_size * mm),
                    stroke_width=1,
                    rx=1 * mm,
                    ry=1 * mm,
                    fill=fill,
                )
            )
            dwg.add(
                dwg.text(
                    text=label,
                    insert=(
                        (x + key_size / 2) * mm,
                        (y + key_size / 2 + maybe_center) * mm,
                    ),
                    font_size="1em",
                    fill="black",
                    text_anchor="middle",
                    font_family="monospace",
                )
            )
            positions.append((x, y))

        # TODO: Make combos own layer maybe?
        # if k == 0:
        if k == 1:
            combo_colors = ["red", "green", "blue", "purple", "pink", "teal"]
            c = 0
            for k1, k2, label in combos:
                k1_x, k1_y = positions[k1]
                k2_x, k2_y = positions[k2]

                if not are_neighbors(k1, k2, columns):
                    print(f"combo {label} not neighborly...")
                    # FIXME: If use circles, have to account for multiple in a location
                    # TODO: Draw legend showing what each combo means
                    # TODO: Number each lil circle so its easier to understand which is which, then
                    # maybe color don't matter, or could be used to denote key count or something?
                    dwg.add(dwg.circle(center=((k1_x + 2) * mm, (k1_y + 2) * mm), r=1 * mm, fill=combo_colors[c]))
                    dwg.add(dwg.circle(center=((k2_x + 2) * mm, (k2_y + 2) * mm), r=1 * mm, fill=combo_colors[c]))
                    # dwg.add(dwg.text(text=label, insert=((k1_x + 2) * mm, (k1_y + 2) * mm)))
                    # dwg.add(dwg.text(text=label, insert=((k2_x + 2) * mm, (k2_y + 2) * mm)))
                    c += 1
                    continue

                height = 5
                width = 10

                x = k2_x - width / 2
                y = (k1_y + k2_y) / 2 + key_size / 2 - height / 2

                dwg.add(
                    dwg.rect(
                        insert=(
                            x * mm,
                            y * mm,
                        ),
                        size=(width * mm, height * mm),
                        rx=1 * mm,
                        ry=1 * mm,
                        fill="beige",
                        fill_opacity=0.8,
                    )
                )

                dwg.add(
                    dwg.text(
                        text=label,
                        insert=(
                            (x + width / 2) * mm,
                            (y + height / 2 + maybe_center / 2) * mm,
                        ),
                        font_size="0.65em",
                        fill="black",
                        text_anchor="middle",
                        font_family="monospace"
                        # dominant_baseline="central"  # no valid?
                    )
                )

        dwg.save()


if __name__ == "__main__":
    keymap("keymap.svg")
