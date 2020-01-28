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
python3-dev \
python3-pip \
python3-nose \
python3-numpy \
python3-scipy \
default-jre \
default-jdk \
curl 

# Set locale to get file encodings right
RUN apt-get install -y locales
RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

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
RUN curl -o $OPENNLP/models/en-pos-maxent.bin http://opennlp.sourceforge.net/models-1.5/en-pos-maxent.bin


# Install bleeding-edge Theano
RUN pip install --upgrade pip
RUN pip install --upgrade six
RUN pip install --upgrade --no-deps git+git://github.com/Theano/Theano.git
RUN pip install joblib gunicorn flask pexpect

RUN pip3 install pexpect tqdm lxml beautifulsoup4



EXPOSE 5000:5000

