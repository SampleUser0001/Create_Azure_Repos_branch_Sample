#!/bin/bash

git_repo_home=$1
target=$2
source=$3

pushd $git_repo_home > /dev/null

git diff --name-status origin/${target}...origin/${source}

popd > /dev/null