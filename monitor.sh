#!/bin/bash

CONTAINER=flask-monitor

STATUS=$(docker inspect -f '{{.State.Running}}' $CONTAINER 2>/dev/null)

if [ "$STATUS" != "true" ]; then
    echo "$(date) : Container stopped. Restarting..." >> logs/incidents.log
    docker restart $CONTAINER
fi