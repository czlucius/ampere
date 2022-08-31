#!/bin/bash
#if [[ $EUID -ne 0 ]]; then
 #  echo "This script must be run as root"
  # exit 1
#fi

poetry update
# (Instruction 1)
# Run the LibreTranslate instance, without a web UI:
# The translate instance will be run on the same device.

# (Instruction 2)
# Start the bot through Poetry. Note that this call is blocking, do not place anything after it, unless it is intended to run after
# the bot has finished operation.
poetry run python3 bot.py & (sudo docker run --platform=linux/amd64 -it --restart=unless-stopped -p 5907:5907 libretranslate/libretranslate --disable-web-ui) && fg