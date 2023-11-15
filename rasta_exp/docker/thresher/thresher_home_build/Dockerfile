FROM ubuntu:14.04

# RUN sed -i -e "s/archive.ubuntu.com/old-releases.ubuntu.com/g" /etc/apt/sources.list

RUN apt-get update && apt-get install -y git time

RUN mkdir /workspace
RUN git init /workspace/thresher && \
    cd /workspace/thresher && \
    git remote add origin https://github.com/cuplv/thresher.git && \
    git fetch --depth=1 origin f1befd23fb5583e5ee257d9a5ea3f42a2ef14c34 && \
    git reset --hard FETCH_HEAD

RUN apt-get update && apt-get install -y make openjdk-6-jdk libgomp1 wget unzip python autoconf g++

RUN cd /workspace/ && \
    wget http://downloads.sourceforge.net/project/dex2jar/dex2jar-2.0-20140818.061505-10.zip && \
    unzip dex2jar-2.0-20140818.061505-10.zip && rm dex2jar-2.0-20140818.061505-10.zip && \
    mv dex2jar-2.0-SNAPSHOT dex2jar

RUN cd /workspace/ && \
    wget -O - https://github.com/sbt/sbt/releases/download/v0.13.18/sbt-0.13.18.tgz | tar xzv && \
    cd sbt && \
    mkdir -p /root/.ivy2/local && \
    cp -r lib/local-preloaded/* /root/.ivy2/local/
# Install deps for ScalaZ3
RUN mkdir -p /root/.sbt/preloaded/org/scalatest/scalatest_2.10/1.9.1 && \
    wget -O /root/.sbt/preloaded/org/scalatest/scalatest_2.10/1.9.1/scalatest_2.10-1.9.1.pom https://repo1.maven.org/maven2/org/scalatest/scalatest_2.10/1.9.1/scalatest_2.10-1.9.1.pom && \
    wget -O /root/.sbt/preloaded/org/scalatest/scalatest_2.10/1.9.1/scalatest_2.10-1.9.1.jar https://repo1.maven.org/maven2/org/scalatest/scalatest_2.10/1.9.1/scalatest_2.10-1.9.1.jar && \
    mkdir -p /root/.sbt/preloaded/org/sonatype/oss/oss-parent/7 && \
    wget -O /root/.sbt/preloaded/org/sonatype/oss/oss-parent/7/oss-parent-7.pom https://repo1.maven.org/maven2/org/sonatype/oss/oss-parent/7/oss-parent-7.pom && \
    mkdir -p /root/.sbt/preloaded/org/scala-lang/scala-library/2.10.2 && \
    wget -O /root/.sbt/preloaded/org/scala-lang/scala-library/2.10.2/scala-library-2.10.2.pom https://repo1.maven.org/maven2/org/scala-lang/scala-library/2.10.2/scala-library-2.10.2.pom && \
    wget -O /root/.sbt/preloaded/org/scala-lang/scala-library/2.10.2/scala-library-2.10.2.jar https://repo1.maven.org/maven2/org/scala-lang/scala-library/2.10.2/scala-library-2.10.2.jar && \
    mkdir -p /root/.sbt/preloaded/org/scala-lang/scala-compiler/2.10.2 && \
    wget -O /root/.sbt/preloaded/org/scala-lang/scala-compiler/2.10.2/scala-compiler-2.10.2.pom https://repo1.maven.org/maven2/org/scala-lang/scala-compiler/2.10.2/scala-compiler-2.10.2.pom && \
    wget -O /root/.sbt/preloaded/org/scala-lang/scala-compiler/2.10.2/scala-compiler-2.10.2.jar https://repo1.maven.org/maven2/org/scala-lang/scala-compiler/2.10.2/scala-compiler-2.10.2.jar && \
    mkdir -p /root/.sbt/preloaded/org/scala-lang/scala-reflect/2.10.2 && \
    wget -O /root/.sbt/preloaded/org/scala-lang/scala-reflect/2.10.2/scala-reflect-2.10.2.pom https://repo1.maven.org/maven2/org/scala-lang/scala-reflect/2.10.2/scala-reflect-2.10.2.pom && \
    wget -O /root/.sbt/preloaded/org/scala-lang/scala-reflect/2.10.2/scala-reflect-2.10.2.jar https://repo1.maven.org/maven2/org/scala-lang/scala-reflect/2.10.2/scala-reflect-2.10.2.jar && \
    mkdir -p /root/.sbt/preloaded/org/scala-lang/jline/2.10.2 && \
    wget -O /root/.sbt/preloaded/org/scala-lang/jline/2.10.2/jline-2.10.2.pom https://repo1.maven.org/maven2/org/scala-lang/jline/2.10.2/jline-2.10.2.pom && \
    wget -O /root/.sbt/preloaded/org/scala-lang/jline/2.10.2/jline-2.10.2.jar https://repo1.maven.org/maven2/org/scala-lang/jline/2.10.2/jline-2.10.2.jar && \
    mkdir -p /root/.sbt/preloaded/org/scala-lang/scala-actors/2.10.7 && \
    wget -O /root/.sbt/preloaded/org/scala-lang/scala-actors/2.10.7/scala-actors-2.10.7.pom https://repo1.maven.org/maven2/org/scala-lang/scala-actors/2.10.7/scala-actors-2.10.7.pom && \
    wget -O /root/.sbt/preloaded/org/scala-lang/scala-actors/2.10.7/scala-actors-2.10.7.jar https://repo1.maven.org/maven2/org/scala-lang/scala-actors/2.10.7/scala-actors-2.10.7.jar

ENV PATH="/workspace/sbt/bin:$PATH"

RUN apt-get update && apt-get install -y libjansi-java && \
    wget -O /workspace/scala-2.10.7.deb https://downloads.lightbend.com/scala/2.10.7/scala-2.10.7.deb && \
    dpkg -i /workspace/scala-2.10.7.deb

RUN sed -i 's#git clone https://github.com/wala/WALA.git#git clone --branch R_1.3.6 https://github.com/wala/WALA.git#' /workspace/thresher/build/install_deps.sh && \
    sed -i 's/mv WALA lib/mv WALA lib \&\& (cd lib\/WALA \&\& git checkout ca3f89eac98a81396fc97452bb7d80d46f9c164c)/' /workspace/thresher/build/install_deps.sh && \
    sed -i 's#git clone https://git01.codeplex.com/z3#git clone --branch z3-4.3.0 https://github.com/Z3Prover/z3.git#' /workspace/thresher/build/install_deps.sh && \
    sed -i 's#git clone https://github.com/psuter/ScalaZ3.git#git clone --branch v2.1 https://github.com/psuter/ScalaZ3.git#' /workspace/thresher/build/install_deps.sh && \
    sed -i 's#Z3_VERSION=.*#Z3_VERSION=4.3-unix-64b#' /workspace/thresher/build/build_deps.sh && \
    sed -i 's#cd $BASE/lib/ScalaZ3/z3/x64/ && mkdir $Z3_VERSION && cd $Z3_VERSION#mkdir -p "$BASE/lib/ScalaZ3/z3/$Z3_VERSION" \&\& cd "$_"#' /workspace/thresher/build/build_deps.sh && \
    sed -i 's#Z3_VERSION =.*#Z3_VERSION = 4.3-unix-64b#' /workspace/thresher/build/Makefile_scalaz3 && \
    cat /workspace/thresher/build/build_deps.sh && \
    sed -i 's#SCALA_VERSION =.*#SCALA_VERSION = 2.10#' /workspace/thresher/build/Makefile_scalaz3 && \
    sed -i 's#sbt package#sbt package \&\& sbt package#' /workspace/thresher/build/Makefile_scalaz3 && \
    sed -i 's#SCALA_VERSION =.*#SCALA_VERSION = 2.10#' /workspace/thresher/Makefile && \
    sed -i 's#/scala_#/scala-#g' /workspace/thresher/build/Makefile_scalaz3 && \
    sed -i 's#/scala_#/scala-#g' /workspace/thresher/Makefile && \
    sed -i 's#LD_LIBRARY_PATH=#LD_LIBRARY_PATH=lib-bin/:#' /workspace/thresher/build/Makefile_scalaz3 && \
    cd /workspace/thresher && \
    make install-deps && \
    sed -i 's#sbt.version=.*#sbt.version=0.13.18#' /workspace/thresher/lib/ScalaZ3/project/build.properties && \
    sed -i 's#scalaVersion := .*#scalaVersion := "2.10.7"#' /workspace/thresher/lib/ScalaZ3/build.sbt && \
    echo "-Dhttps.protocols=TLSv1.2" > /workspace/thresher/lib/ScalaZ3/.jvmopts && \
    sed -i 's#2.10.2#2.10.2#' /workspace/thresher/lib/ScalaZ3/build.sbt && \
    cd /workspace/thresher/lib/z3 && \
    autoconf && \
    /workspace/thresher/lib/z3/configure && \
    cd /workspace/thresher && \
    make deps && \
    mkdir /workspace/thresher/bin && \
    make && \
    make tests && \
    sed -i 's#LD_LIBRARY_PATH=#LD_LIBRARY_PATH=$THRESHER_HOME/lib/ScalaZ3/lib-bin/:#' /workspace/thresher/thresher.sh && \
    sed -i 's#SCALA_VERSION=.*#SCALA_VERSION=2.10#' /workspace/thresher/thresher.sh && \
    sed -i 's#Z3_VERSION=.*#Z3_VERSION=4.3-unix-64b#' /workspace/thresher/thresher.sh && \
    sed -i 's#/scala_#/scala-#g' /workspace/thresher/thresher.sh && \
    sed -i 's#java -cp .:#java -cp .:lib/ScalaZ3/jar-releases/64/scala-2.9.1/scalaz3-3.2.c.jar:#g' /workspace/thresher/thresher.sh
