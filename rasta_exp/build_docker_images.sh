#!/usr/bin/env bash


SIF_DIR=$1
if [[ -z "${SIF_DIR}" ]]; then 
    echo MISSING SIF_DIR parameter
    exit 1
fi

[[ -d "${SIF_DIR}" ]] || mkdir "${SIF_DIR}"

function docker_to_sif {
    img_name=$1
    [[ -f ${SIF_DIR}/$1.sif ]] && rm ${SIF_DIR}/$1.sif
    singularity pull ${SIF_DIR}/$1.sif docker-daemon:$1:latest 
}


function build_docker_img {
    pushd .
    tool_name=$1
    cd docker/${tool_name}
    version=$(cat RASTA_VERSION)
    cd ${version}
    docker build --ulimit nofile=65536:65536 -f Dockerfile -t rasta-${tool_name} .
    docker save rasta-${tool_name}:latest | gzip > ../../../${SIF_DIR}/rasta-${tool_name}.tar.gz
    popd
}

# Final list:
#tools="androguard androguard_dad didfail adagio anadroid blueseal didfail flowdroid mallodroid redexer saaf wognsen_et_al iccta ic3 ic3_fork gator droidsafe apparecium amandroid dialdroid perfchecker"
tools="androguard androguard_dad didfail adagio anadroid blueseal didfail flowdroid mallodroid redexer saaf wognsen_et_al iccta ic3 ic3_fork gator droidsafe apparecium amandroid dialdroid"

for tool in ${tools}; do
    build_docker_img ${tool}
    docker_to_sif rasta-${tool}
done;
