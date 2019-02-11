FROM ubuntu:18.04

# Install build-essential, git, wget, python-dev, pip, BLAS + LAPACK and other dependencies
RUN apt-get update && apt-get install -y \
build-essential \
gfortran \
git \
wget \
liblapack-dev \
libopenblas-dev \
python-dev \
python-pip \
python-nose \
python-numpy \
python-scipy \
default-jre \
default-jdk \
curl

ENV workdir /usr/src/myapp
RUN mkdir -p $workdir
WORKDIR $workdir

RUN curl -o $workdir/apache-opennlp-1.8.4-bin.tar.xz https://archive.apache.org/dist/opennlp/opennlp-1.8.4/apache-opennlp-1.8.4-bin.tar.gz
RUN tar xzf apache-opennlp-1.8.4-bin.tar.xz
RUN rm apache-opennlp-1.8.4-bin.tar.xz
RUN mv apache-opennlp-1.8.4/ /usr/bin/

ENV OPENNLP /usr/bin/apache-opennlp-1.8.4

RUN mkdir -p $OPENNLP/models
RUN curl -o $OPENNLP/models/en-sent.bin http://opennlp.sourceforge.net/models-1.5/en-sent.bin
RUN curl -o $OPENNLP/models/en-token.bin http://opennlp.sourceforge.net/models-1.5/en-token.bin


# Install bleeding-edge Theano
RUN pip install --upgrade pip
RUN pip install --upgrade six
RUN pip install --upgrade --no-deps git+git://github.com/Theano/Theano.git
RUN pip install joblib gunicorn flask pexpect

EXPOSE 5000:5000

