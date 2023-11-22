#!/bin/bash

git_repo_home=$1
feature=$2

pushd $git_repo_home > /dev/null

git checkout -b ${feature}
git push --set-upstream origin ${feature}

popd > /dev/null