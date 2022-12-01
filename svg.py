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

# start with only adding combos for items next to eachother horizontally
# probably just make a list of combos without box in a legend or something
# then do vertically
# then maybe diagonally
# then separated

layers = [
    """
      4/q     w       f     p b j l u y '
      a       alt/r   cmd/s t g m n e i o
      z       x       c     d v k h , . /
      ctl/esc sft/bsp 1/spc 2/-
    """,
    """
      1 2  3      4 5 6 7 8 9 0
      ! @  #      $ % ^ & * = :
      ~ ;  '      " | + ( { [ \\
      ` <tr> <held> <tr>
    """,
    """
      <tr> <tr> <tr>  <tr>  <tr> mute vol- vol+ <tr> sleep
      <tr> <tr> c+s+← c+s+→ <tr> ←    ↓    ↑    →    <tr>
      <tr> <tr> c+a+← c+s+→ <tr> <tr> <tr> <tr> <tr> <tr>
      <tr> <tr> <tr>  <held>
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
    [6, 7, "save"],
    [21, 22, "copy"],
    [22, 23, "paste"],
    [21, 23, "cut"],
    [26, 27, "enter"],
    [27, 28, "capsword"],
]

y_offsets = [10, 5, 0, 5, 5, 5, 5, 0, 5, 10]

spacing = 19
key_size = 18
maybe_center = 1


def are_neighbors(k1, k2, columns):
    return k2 - k1 == 1 and k2 % columns != 0


def keymap(name):
    dwg = svgwrite.Drawing(filename=name, debug=True, profile="tiny")
    for l, layer in enumerate(layers):
        keys = layer.split()

        positions = []

        for i in range(34):
            row, col = divmod(i, 10)

            # TODO: Handle thumb row better
            if i >= 30:
                col += 3

            x = 10 + (col * spacing)
            y = 10 + (l * 85) + (row * spacing) + y_offsets[col]

            if col >= 5:
                x += 15

            label = keys[i]
            fill = "lightgray"

            if label == "<held>":
                fill = "khaki"
                label = ""

            if label == "<tr>":
                label = "▽"

            # TODO: Can't just enter newlines, have to do something fancier
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

        if l == 0:
            for k1, k2, label in combos:
                if not are_neighbors(k1, k2, columns):
                    print(f"combo {label} not neighborly...")
                    continue

                _, k1_y = positions[k1]
                k2_x, k2_y = positions[k2]

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
                    )
                )

                dwg.add(
                    dwg.text(
                        text=label,
                        insert=(
                            (x + width / 2) * mm,
                            (y + height / 2 + maybe_center / 2) * mm,
                        ),
                        font_size="0.5em",
                        fill="black",
                        text_anchor="middle",
                        font_family="monospace"
                        # dominant_baseline="central"  # no valid?
                    )
                )

        dwg.save()


if __name__ == "__main__":
    keymap("keymap.svg")
