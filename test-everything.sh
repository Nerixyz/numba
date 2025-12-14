#!/bin/sh

set -ex

export IRHASH_CACHE="${IRHASH_CACHE:-/tmp/irhash}"
export IRTEST_OUT="${IRTEST_OUT:-/tmp/irtest}"

./clean-everything.sh

myprocs=$(nproc)
myprocs=$((myprocs>12 ? myprocs - 4 : myprocs))

export IRTEST_MODE=numba-nocache
export IRTEST_PHASE=0
echo "$IRTEST_MODE @ $IRTEST_PHASE"
make -j$myprocs

export IRTEST_MODE=numba-cache
export IRTEST_PHASE=0
echo "$IRTEST_MODE @ $IRTEST_PHASE"
make -j$myprocs

export IRTEST_MODE=numba-cache
export IRTEST_PHASE=1
echo "$IRTEST_MODE @ $IRTEST_PHASE"
make -j$myprocs

export IRTEST_MODE=irhash
export IRTEST_PHASE=0
echo "$IRTEST_MODE @ $IRTEST_PHASE"
make -j$myprocs

export IRTEST_MODE=irhash
export IRTEST_PHASE=1
echo "$IRTEST_MODE @ $IRTEST_PHASE"
make -j$myprocs

echo "done."
