#!/bin/sh

set -ex

./test-everything.sh
python x_irhash/reduce.py
