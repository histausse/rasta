
SIF_DIR=$1
TOOL=$2
if [[ -z "${SIF_DIR}" ]]; then
    echo MISSING SIF_DIR parameter
    echo 'usage:  ./quick_test_tool.sh SID_DIR TOOL'
    exit 1
fi
if [[ -z "${TOOL}" ]]; then
    echo MISSING TOOL parameter
    echo 'usage:  ./quick_test_tool.sh SID_DIR TOOL'
    exit 1
fi

mkdir -p "/tmp/RASTA/${TOOL}"

while read apk; do
    python grunt-worker.py --base-dir "/tmp/RASTA/${TOOL}"  --no-mark-done --keep-tmp-dir --no-write-to-couch --manual --task ${TOOL} --sha ${apk} --singularity --image-basedir ${SIF_DIR}
done <"apks_${TOOL}.txt"
