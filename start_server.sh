docker pull huner/huner:master;
docker kill "$1" 2> /dev/null > /dev/null;
docker rm "$1" 2> /dev/null > /dev/null;
docker run -p 5000 -t -i --name "$1" --volume ${PWD}:/usr/huner huner/huner:master /bin/bash -c "cd /usr/huner; python tagger.py $1"
