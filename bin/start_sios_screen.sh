#!/bin/bash

NL=`echo -ne '\015'`
SIOS_CMD="cd /opt/stack/rebac; /opt/stack/rebac/bin/rebac-api --config-file=/etc/rebac/rebac-api.conf || touch \"/opt/stack/status/stack/rebac-api.failure\""
SIOS_LOGFILE="/opt/stack/logs/screen/screen-rebac.log"
SCREEN=$(which screen)
if [[ -n "$SCREEN" ]]; then
    SESSION=$(screen -ls | awk '/[0-9].stack/ { print $1 }')
    if [[ -n "$SESSION" ]]; then
        screen -S $SESSION -X screen -t rebac bash
        screen -S $SESSION -p rebac -X logfile $SIOS_LOGFILE
        screen -S $SESSION -p rebac -X log on
        screen -S $SESSION -p rebac -X stuff "$SIOS_CMD $NL"
    fi
fi

