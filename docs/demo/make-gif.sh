#!/bin/sh
# MP4 -> README GIF: 15 fps, 960 px wide, one shared palette.
set -e
ffmpeg -y -i out/demo.mp4 -vf "fps=15,scale=960:-1:flags=lanczos,palettegen=max_colors=128:stats_mode=diff" out/palette.png
ffmpeg -y -i out/demo.mp4 -i out/palette.png \
  -lavfi "fps=15,scale=960:-1:flags=lanczos[x];[x][1:v]paletteuse=dither=bayer:bayer_scale=4:diff_mode=rectangle" \
  ../assets/demo.gif
ls -lh ../assets/demo.gif
