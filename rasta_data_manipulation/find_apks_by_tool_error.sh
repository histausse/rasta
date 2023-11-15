#!/usr/bin/env sh

PWD=$(pwd)
TOOL=${1}
ERROR=${2}
DATABASE=${3:-'rasta.db'}
REPORT_FOLDER=${4:-"$PWD/../data/reports/rasta"}

USAGE=$(cat <<- EOM
usage: ${0} <tool> <error> [<database> [<repport folder>]]
EOM
)

if [[ -z "$TOOL" ]] || [[ -z "$ERROR" ]] || [[ -z "$DATABASE" ]] || [[ -z "$REPORT_FOLDER" ]] ; then
    echo ${USAGE}
    exit 1
fi

TMP_FILE=$(mktemp)
sqlite3 ${DATABASE} "SELECT DISTINCT error.sha256 || '_-_' || error.tool_name FROM error INNER JOIN exec ON error.tool_name = exec.tool_name AND error.sha256 = exec.sha256 WHERE exec.tool_status = 'FAILED' AND error.tool_name = '$TOOL' and error = '$ERROR';" > ${TMP_FILE}

find ${REPPORT_FOLDER} | grep -F -f ${TMP_FILE}
rm ${TMP_FILE}


