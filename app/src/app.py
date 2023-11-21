# -*- coding: utf-8 -*-
from logging import getLogger, config, StreamHandler, DEBUG
import os

# import sys
from logutil import LogUtil
from importenv import ImportEnvKeyEnum
from datetime import datetime

# from util.sample import Util
from util import Util
from controller import CreateBranchController, GetRepositoryIdController, CreatePullRequestController
from model import CreatePullRequestModel

PYTHON_APP_HOME = os.getenv('PYTHON_APP_HOME')
LOG_CONFIG_FILE = ['config', 'log_config.json']

logger = getLogger(__name__)
log_conf = LogUtil.get_log_conf(os.path.join(PYTHON_APP_HOME, *LOG_CONFIG_FILE))
config.dictConfig(log_conf)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False

BRANCH_DATE = datetime.now().strftime('%Y%m%d_%H%M')

if __name__ == '__main__':
    # 起動引数の取得
    # args = sys.argv
    # args[0]はpythonのファイル名。
    # 実際の引数はargs[1]から。
    
    # print('Hello Python on Docker!!')
    logger.info('Start.')

    # .envの取得
    # print(ImportEnvKeyEnum.SAMPLE.value)
    config_path = os.path.join(PYTHON_APP_HOME, 'config', 'repos.json')
    logger.info(f'config : {config_path}')
    
    # リポジトリ一覧を取得
    repo_list = Util.load_repos(os.path.join(PYTHON_APP_HOME, 'config', 'repos.json'))
    
    logger.debug(repo_list)
    for repo in repo_list:
        repo_name = repo.repo_name
        logger.info(f'repo name : {repo_name}')

        repo_id_getter = GetRepositoryIdController()
        repo_id = repo_id_getter.getId(repo_name)
        logger.debug(f'repo id : {repo_id}')
        for branch in repo.branches:
            try:
                logger.info(f'1st : {branch.source} , 2nd : {branch.target}')
                create_branch = CreateBranchController(repo_name, branch, BRANCH_DATE)
                feature_branch = create_branch.create_branch()
                logger.info(f'Created branch : {feature_branch}')

                create_pull_request_model = CreatePullRequestModel(
                    repo_name=repo_name, repo_id=repo_id,
                    branch=branch, branch_date=BRANCH_DATE,
                    pull_request_source_branch=feature_branch,
                    requred=[], optional=[]
                )
                create_pull_request_controller = CreatePullRequestController(create_pull_request_model)
                pull_request_url = create_pull_request_controller.create()
                logger.info(f'Pull request URL : {pull_request_url}')
            except Exception as e:
                logger.error(e)
