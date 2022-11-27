FROM ubuntu:20.04 as build_stage

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        build-essential \
        python3 \
        python3-pip \
        && \
    rm -rf /var/lib/apt/lists/*



WORKDIR /pypapi

COPY papi papi

WORKDIR /pypapi/papi/src

ENV CFLAGS="-fPIC -Werror=format-truncation=0"
ENV PAPI_COMPONENTS="net perf_event perf_event_uncore powercap rapl"
RUN ./configure --with-components=${PAPI_COMPONENTS} && \
    make

WORKDIR /pypapi

RUN pip install cffi==1.15.1 numpy==1.23.5

COPY setup.py setup.py

COPY pypapi pypapi

RUN python3 pypapi/papi_build.py

RUN pip install .
