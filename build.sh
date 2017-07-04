#!/bin/bash

export CFLAGS="-fPIC"
export CXXFLAGS="-fPIC"

cd ./papi/src/libpfm4
make clean
cd -

cd ./papi/src/libpfm-3.y
make clean
cd -

cd ./papi/src
./configure CFLAGS="-fPIC" CXXFLAGS="-fPIC"
make clean
make -j 2
cd -

python pypapi/papi_build.py
