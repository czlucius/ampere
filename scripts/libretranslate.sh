# Enable ARM64 -> AMD64 emulation (LibreTranslate does not work on ARM64, but emulation works well)
sudo docker run --privileged tonistiigi/binfmt --install amd64

sudo docker run --platform=linux/amd64 -it --restart=unless-stopped -p 5907:5907 libretranslate/libretranslate --disable-web-ui