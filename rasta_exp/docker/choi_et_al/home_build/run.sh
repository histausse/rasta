#!/bin/sh

chown -R nix /mnt
# Run jadx on /mnt/app.apk
HOME=/home/nix sudo -u nix bash -c '. /home/nix/.nix-profile/etc/profile.d/nix.sh && cd /mnt && nix-shell -p jadx --run "jadx app.apk"'
find /mnt/app -name '*.java' -print | xargs /workspace/JavaAnalysis/Main
