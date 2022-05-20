# FROM ubuntu:18.04
FROM nvidia/cuda:10.2-cudnn7-runtime-ubuntu18.04
ENV PATH="/root/Anaconda3/bin:${PATH}"
ARG PATH="/root/Anaconda3/bin:${PATH}"

RUN apt update \
	&& apt install -y htop python3-dev wget

RUN wget https://repo.continuum.io/archive/Anaconda3-2018.12-Linux-x86_64.sh \
	&& mkdir root/.conda \
	&& sh Anaconda3-2018.12-Linux-x86_64.sh -b \
	&& rm -f Anaconda3-2018.12-Linux-x86_64.sh

RUN conda create -y -n ml python=3.7

COPY . src/
RUN /bin/bash -c "cd src \
	&& source activate ml \
	&& pip install -r requirements.txt"