#!/bin/bash

git_dir=$1
repo_name=$2
git_url=$3
source_branch=$4

# Tokenを60秒だけ受け入れるようにする。使用している環境の認証方法に応じて設定する。
git config --global credential.helper 'cache --timeout=60'

pushd $git_dir > /dev/null

git clone -b $source_branch $git_url

popd > /dev/null