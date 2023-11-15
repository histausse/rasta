FROM ubuntu:22.04

# RUN sed -i -e "s/archive.ubuntu.com/old-releases.ubuntu.com/g" /etc/apt/sources.list

RUN apt-get update && apt-get install -y git time

RUN mkdir /workspace
RUN git init /workspace/redexer && \
    cd /workspace/redexer && \
    git remote add origin https://github.com/plum-umd/redexer.git && \
#    git fetch --depth=1 origin f80520d5310bf80fdd204c1c03b30278982a4431 && \
    git fetch --depth=1 origin 60c9324b9ff2ffc27c377069fa5b54f097bf7e64 && \
    git reset --hard FETCH_HEAD

RUN apt-get update && apt-get install -y ocaml opam sdkmanager android-sdk ruby ruby-rubygems apktool ocamlbuild && \
    opam -y init && \
    eval $(opam config env) && \
    opam -y install sha ppx_deriving ppx_deriving_yojson yojson && \
    opam -y pin add yojson 1.7.0 && \
    gem install nokogiri

# replace `eval $(opam config env)`
ENV OPAM_SWITCH_PREFIX "/root/.opam/default"
ENV CAML_LD_LIBRARY_PATH "/root/.opam/default/lib/stublibs:/usr/local/lib/ocaml/4.13.1/stublibs:/usr/lib/ocaml/stublibs"
ENV OCAML_TOPLEVEL_PATH "/root/.opam/default/lib/toplevel"
ENV MANPATH "/root/.opam/default/man"
ENV PATH "/root/.opam/default/bin:$PATH"

# Set Path for android Tools
env ANDROID_HOME "/usr/lib/android-sdk"
env PATH "$PATH:$ANDROID_HOME/tools"
env PATH "$PATH:$ANDROID_HOME/platform-tools"
env PATH "$PATH:$ANDROID_HOME/build-tools/29.0.3"

RUN cd /workspace/redexer && make clean && make

COPY run.sh /
