#!/bin/bash
# check.sh, run 60 times, internal time is 1 min
# 0 * * * * /home/check_xu.sh
# or
# scp check.sh /etc/cron.hourly/
DAT="`date +%Y%m%d`"
HOUR="`date +%H`"
LOCAL_IP=$(ifconfig $VAR | grep "inet addr" | grep -v '127.0.0.1' | awk '{ print $2}' | awk -F: '{print $2}')
DIR="/opt/perflog_${LOCAL_IP}"

# check cycle: 1 min
DELAY=60
# check times: 60
COUNT=60
# whether the responsible directory exist
if ! test -d ${DIR}
then
    /bin/mkdir -p ${DIR}
fi
# general check
export TERM=linux
/usr/bin/top -b -d ${DELAY} -n ${COUNT} > ${DIR}/top_${DAT}.log 2>&1 &
# cpu check
#/usr/bin/sar -u ${DELAY} ${COUNT} > ${DIR}/cpu_${DAT}.log 2>&1 &
#/usr/bin/mpstat -P 0 ${DELAY} ${COUNT} > ${DIR}/cpu_0_${DAT}.log 2>&1 &
#/usr/bin/mpstat -P 1 ${DELAY} ${COUNT} > ${DIR}/cpu_1_${DAT}.log 2>&1 &
# memory check
#/usr/bin/vmstat ${DELAY} ${COUNT} > ${DIR}/vmstat_${DAT}.log 2>&1 &
