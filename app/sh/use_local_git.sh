#!/bin/bash

git_url=$1
repo_name=$2
source_branch=$3
feature_branch=$4

# Tokenを30秒だけ受け入れるようにする。使用している環境の認証方法に応じて設定する。
git config --global credential.helper 'cache --timeout=30'

tmp_work_dir=/tmp/$(uuidgen)
mkdir $tmp_work_dir
pushd $tmp_work_dir

git clone -b ${source_branch} $git_url

cd $repo_name
git checkout -b ${feature_branch}
git push --set-upstream origin ${feature_branch}

popd > /dev/null
rm -rf $tmp_work_dir
