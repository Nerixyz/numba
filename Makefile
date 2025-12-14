# TESTS := $(shell cat all-tests.txt)
# TESTS := $(shell cat with-cache.txt)
# TESTS := $(shell cat rand-tests.txt)
TESTS := $(shell cat 100-tests.txt)

IRTEST_OUT ?= /tmp/irtest

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
