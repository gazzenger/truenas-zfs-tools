#!/bin/bash

## Script to unlock TrueNAS dataset(s) by way of typed passphrase

set -e

# get dir of this script to load conf
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

. $DIR/.env

# the following should be defined in conf file:
#SSH_HOST=
#SSH_USER=
#datasets=()

#check for input arg $1
# $1: lock or unlock, unlock is the default
ACTION=${1:-unlock}

for dataset in "${datasets[@]}"; do
  if [ "$ACTION" == "lock" ]; then
    echo -n "Locking $dataset..."
    ssh $SSH_USER@$SSH_HOST "midclt call pool.dataset.lock \"${dataset}\" &> /dev/null"
  else
    read -s -p "Enter passphrase for dataset $dataset: " PASS
    echo
    echo -n "Unlocking $dataset..."
    ssh $SSH_USER@$SSH_HOST "midclt call pool.dataset.unlock \"${dataset}\" \"{\\\"datasets\\\": [{\\\"name\\\": \\\"${dataset}\\\",\\\"passphrase\\\": \\\"\"'${PASS}'\"\\\"}]}\" &> /dev/null"
  fi

# Sleep 5s before checking if it is unlocked
  sleep 5s
  RESULT=$(ssh $SSH_USER@$SSH_HOST "midclt call pool.dataset.query \"[[\\\"id\\\", \\\"=\\\", \\\"${dataset}\\\"]]\" | jq '.[0].locked'")
  if [ "$ACTION" == "lock" ]; then
    if [[ "$RESULT" == "true" ]]; then echo "Success"; else echo "Failed"; fi
  else
    if [[ "$RESULT" == "true" ]]; then echo "Failed"; else echo "Success"; fi 
  fi

  echo
done

