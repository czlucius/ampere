
#!/bin/bash
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root"
   exit 1
fi
# The commands below require superuser access.

# Enable ARM64 -> AMD64 emulation (LibreTranslate does not work on ARM64, but emulation works well)
docker run --privileged tonistiigi/binfmt --install amd64

