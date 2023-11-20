#!/bin/bash

git_url=$1
repo_name=$2

# Tokenを30秒だけ受け入れるようにする。使用している環境の認証方法に応じて設定する。
# git config --global credential.helper 'cache --timeout=30'

tmp_work_dir=/tmp/$(uuidgen)
mkdir $tmp_work_dir
pushd $tmp_work_dir

git clone -b develop $git_url

cd $repo_name
branch_date=$(date "+%Y%m%d_%H%M")
git checkout -b feature/merge_to_develop_2_${branch_date}
git push --set-upstream origin feature/merge_to_develop_2_${branch_date}

popd > /dev/null
rm -rf $tmp_work_dir
