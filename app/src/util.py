# -*- coding: utf-8 -*-
from logging import getLogger, config, StreamHandler, DEBUG
import os

# import sys
from logutil import LogUtil
from importenv import ImportEnvKeyEnum

import json
from typing import List

from model import RepositoryModel, BranchModel, ExportModel

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

class Util():
    @staticmethod
    def load_repos(json_path: str) -> [RepositoryModel]:
        return_list = []
        with open(json_path, 'r') as fp:
            json_data = json.load(fp=fp)
            return_list = [RepositoryModel.from_dict(model) for model in json_data]
        return return_list
    
    @staticmethod
    def generate_pull_request_source_branch(branch: BranchModel, branch_date: str) -> str:
        """
        sourceブランチ名を作成する。
        git checkoutとプルリクエスト作成で使えるやつ。
        """
        return f'{branch.feature}/merge_to_{branch.target}_{branch_date}'
        
    @staticmethod
    def export(filepath:str, branch_date:str, list: List[ExportModel]) -> None:
        with open(filepath, encoding='utf-8', mode='w') as f:
            f.write(f'# {branch_date}' + '\n')
            f.write('\n')
            f.write('| Repository | Source Branch | Target Branch | Pull Requrest URL |' + '\n')
            f.write('| :--------- | :------------ | :------------ | :---------------- |' + '\n')
            for _ in list:
                f.write(f'| {_.repo_name} | {_.source} | {_.target} | {_.pull_request_url} | \n') 
            f.write('\n')
