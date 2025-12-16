#!/bin/sh

set -ex;

IRHASH_CACHE="${IRHASH_CACHE:-/tmp/irhash}"
IRTEST_OUT="${IRTEST_OUT:-/tmp/irtest}"

rm -rf **/*/__pycache__
rm -rf "$IRHASH_CACHE"
rm -rf "$IRTEST_OUT"

mkdir -p $IRHASH_CACHE
mkdir -p "$IRTEST_OUT/numba-nocache-0"
mkdir -p "$IRTEST_OUT/numba-cache-0"
mkdir -p "$IRTEST_OUT/numba-cache-1"
mkdir -p "$IRTEST_OUT/irhash-0"
mkdir -p "$IRTEST_OUT/irhash-1"
