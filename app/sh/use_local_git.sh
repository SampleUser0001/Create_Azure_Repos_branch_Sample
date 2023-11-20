#!/bin/bash

git_url=$1
repo_name=$2
target_branch=$3
source_branch=$4
feature_name=$5
branch_date=$6

# Tokenを30秒だけ受け入れるようにする。使用している環境の認証方法に応じて設定する。
# git config --global credential.helper 'cache --timeout=30'

tmp_work_dir=/tmp/$(uuidgen)
mkdir $tmp_work_dir
pushd $tmp_work_dir

git clone -b ${source_branch} $git_url

cd $repo_name
git checkout -b ${feature_name}/merge_to_${target_branch}_${branch_date}
git push --set-upstream origin ${feature_name}/merge_to_${target_branch}_${branch_date}

popd > /dev/null
rm -rf $tmp_work_dir
