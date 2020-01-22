#!/usr/bin/env bash

MODEL=$1
TRAIN=$2
DEV=$3
TEST=$4


docker pull huner/huner;
docker kill "$1" 2> /dev/null > /dev/null;
docker rm "$1" 2> /dev/null > /dev/null;

docker run -t -i --volume ${PWD}:/usr/huner huner/huner /bin/bash -c "cd /usr/huner; python train.py --train "$TRAIN" --dev "$DEV" --test "$TEST" -s iob --dropout 0.3 --word_dim 200 --lr_method sgd-lr_.005 --model_path "$MODEL" --reload 1"
