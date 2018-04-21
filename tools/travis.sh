#!/bin/bash
#
# Run the build mode specified by the BUILD variable, defined in
# .travis.yml. When the variable is unset, assume we should run the
# standard test suite.

rootdir=$(dirname $(dirname $0))

# Show the commands being run.
set -x

# Exit on any error.
set -e

case "$BUILD" in
    docs)
        python setup.py build_sphinx;;
    linter)
        flake8;;
    *)
        pytest -v \
               --cov=imapautofiler \
               --cov-report term-missing \
               --cov-config $rootdir/.coveragerc \
               $@;;
esac
