#!/usr/bin/env bash

TRAIN=$1
DEV=$2
TEST=$3


docker pull huner/huner;
docker kill "$1" 2> /dev/null > /dev/null;
docker rm "$1" 2> /dev/null > /dev/null;

docker run -t -i --volume ${PWD}:/usr/huner huner/huner /bin/bash -c "cd /usr/huner; python train_no_finetune.py --train "$TRAIN" --dev "$DEV" --test "$TEST" -s iob --dropout 0.3 --word_dim 200 --lr_method sgd-lr_.005"
