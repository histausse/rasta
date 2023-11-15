FROM ubuntu:14.04

#RUN sed -i -e "s/archive.ubuntu.com/old-releases.ubuntu.com/g" /etc/apt/sources.list

RUN apt-get update && apt-get install -y time git

RUN mkdir /workspace && git init /workspace/JavaAnalysis && \
    cd /workspace/JavaAnalysis && \
    git remote add origin https://github.com/kwanghoon/JavaAnalysis.git && \
    git fetch --depth=1 origin fba12cc22338b6f425a0c71168dc55afe964345d && \
    git reset --hard FETCH_HEAD

RUN apt-get update && apt-get install -y ghc libghc-mtl-dev

RUN cd /workspace/JavaAnalysis && \
    ghc Main

# Install JADX to convert apk to .java
# Use nixpkgs because older versions of jadx are really unstable and the more
# recent version require java 8, which is not available on ubuntu 14, which is the 
# only distro I fond that can compile and run this tool
RUN apt-get update && apt-get install -y curl xz-utils && \
    useradd -b /home -G sudo -m nix && \
    echo 'nix ALL=(ALL) NOPASSWD:ALL' | EDITOR='tee -a' visudo && \
    HOME=/home/nix sudo -u nix bash -c 'sh <(curl -k -L https://nixos.org/nix/install) --no-daemon' && \
    HOME=/home/nix sudo -u nix bash -c '. /home/nix/.nix-profile/etc/profile.d/nix.sh && nix-env -iA nixpkgs.jadx'

COPY run.sh /workspace/run.sh
