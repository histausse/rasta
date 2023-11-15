
SIF_DIR=$1
DATASET=$2
RESULT_DIR=$3
if [[ -z "${SIF_DIR}" ]]; then
    echo MISSING SIF_DIR parameter
    echo 'usage:  ./quick_test_tool.sh SID_DIR DATASET RESULT_DIR'
    exit 1
fi
if [[ -z "${DATASET}" ]]; then
    echo MISSING DATASET parameter
    echo 'usage:  ./quick_test_tool.sh SID_DIR DATA_SET RESULT_DIR'
    exit 1
fi
if [[ -z "${RESULT_DIR}" ]]; then
    echo MISSING RESULT_DIR parameter
    echo 'usage:  ./quick_test_tool.sh SID_DIR DATA_SET RESULT_DIR'
    exit 1
fi

mkdir -p ${RESULT_DIR}

SIF_DIR="$(readlink -f "$SIF_DIR")"
DATASET="$(readlink -f "$DATASET")"
RESULT_DIR="$(readlink -f "$RESULT_DIR")"
SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"

#tools="androguard androguard_dad didfail adagio anadroid blueseal didfail flowdroid mallodroid redexer saaf wognsen_et_al iccta ic3 ic3_fork gator droidsafe apparecium amandroid dialdroid perfchecker"
tools="androguard androguard_dad didfail adagio anadroid blueseal didfail flowdroid mallodroid redexer saaf wognsen_et_al iccta ic3 ic3_fork gator droidsafe apparecium amandroid dialdroid"

mkdir -p "/tmp/RASTA/"

pushd .
cd ${SCRIPT_DIR}
for tool in ${tools}; do
    while read apk; do
        python "grunt-worker.py" --base-dir "/tmp/RASTA/" --result-dir ${RESULT_DIR} --no-mark-done --no-write-to-couch --manual --task ${tool} --sha ${apk} --singularity --image-basedir ${SIF_DIR}
    done <"${DATASET}";
done;
popd
