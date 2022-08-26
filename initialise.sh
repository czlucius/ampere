#!/bin/bash
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root"
   exit 1
fi

# For Translate: set up the models
# ARM64 -> AMD64 if needed:
docker run --privileged tonistiigi/binfmt --install amd64

# Run the LibreTranslate instance, without a web UI:
# The translate instance will be run on the same device
# TODO: this may be a blocking call!
docker run -it -p --restart=unless-stopped 5000:5000 libretranslate --disable-web-ui

# Start the bot through Poetry. Note that this call is blocking, do not place anything after it, unless it is intended to run after
# the bot has finished operation.
poetry run python3 bot.py