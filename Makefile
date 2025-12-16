TESTS := $(shell cat all-tests.txt)

IRTEST_OUT ?= /tmp/irtest

# Requires
# IRTEST_MODE={numba-nocache,numba-cache,irhash}
# IRTEST_PHASE={0,1}
# IRHASH_CACHE=/tmp/irhash

.PHONY: $(TESTS) all

all: $(TESTS)

$(TESTS):
	@echo "[$(IRTEST_MODE)-$(IRTEST_PHASE)] Running $@"
	@LOG="$(IRTEST_OUT)/$(IRTEST_MODE)-$(IRTEST_PHASE)/irtest-$@.txt"; \
	IRTEST_LOG="$$LOG" ./runtests.py -q "$@" > /dev/null 2>&1 \
		|| (rm -f "$$LOG" && touch "$$LOG.fail")
