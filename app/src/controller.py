# -*- coding: utf-8 -*-
from logging import getLogger, config, StreamHandler, DEBUG
import os

# import sys
from logutil import LogUtil
from importenv import ImportEnvKeyEnum

from model import BranchModel, CreatePullRequestModel
import requests

from util import Util
import json
import base64

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

CREATE_BRANCH_SH = os.path.join(PYTHON_APP_HOME, 'sh', 'use_local_git.sh')
class CreateBranchController():
    """
    _1ブランチから_2ブランチへマージするためのブランチを作成する。
    """
    def __init__(self, repo_name:str, branch: BranchModel, branch_date: str):
        self.repo_name = repo_name
        self.branch = branch
        self.branch_date = branch_date
        
    def create_branch(self) -> str:
        """
        _1ブランチから_2ブランチへマージするためのブランチを作成する。

        Returns:
            str: 作成したブランチ名
        """
        git_url = ImportEnvKeyEnum.GIT_CLONE_URL.value + '/' + self.repo_name
        repo_name = self.repo_name
        source_branch = self.branch.source
        feature_branch = Util.generate_pull_request_source_branch(self.branch, self.branch_date)
        
        stream = os.popen(
            f'{CREATE_BRANCH_SH} \
            {git_url} \
            {repo_name} \
            {source_branch} \
            {feature_branch} ')

        logger.info(stream.read())
        
        return feature_branch

class GetRepositoryIdController():
    """
    リポジトリIDを取得する。
    リポジトリIDはAPIを実行して取得する。
    オブジェクト内で取得した履歴を持ち、2回目以降は履歴から返す。
    """
    def __init__(self):
        self.id_dict = {}
    
    def getId(self, repo: str):
        if repo in self.id_dict:
            return self.id_dict[repo]
        else:
            result = requests.get(
                self.getURL(
                    ImportEnvKeyEnum.ORGANIZATION.value,
                    ImportEnvKeyEnum.PROJECT_NAME.value
                ),
                auth=('git',ImportEnvKeyEnum.TOKEN.value)
            ).json()

            logger.debug(result)

            id = result['value'][0]['id']
            self.id_dict[repo] = id

            logger.info(f'RepositoryId , {repo} : {id}')
            
            return id

    def getURL(self, organization:str, project:str) -> str:
        return f'https://dev.azure.com/{organization}/{project}/_apis/git/repositories?api-version=7.0'
    
class CreatePullRequestController():
    """プルリクエストを生成する。
    """
    def __init__(self, pull_request_model: CreatePullRequestModel):
        self._ = pull_request_model

    def create(self) -> str:
        """プルリクエストを作成する。作成にAPIを使用する。

        Returns:
            str: 作成したプルリクエストのURLを返す。
        """
        
        auth_word=f'git:{ImportEnvKeyEnum.TOKEN.value}'
        encoded=base64.standard_b64encode(auth_word.encode())
        
        
        headers = {
            "Authorization": f"Basic {encoded.decode()}",
            "Content-Type": "application/json"
        }
        body = {
            "sourceRefName": f"refs/heads/{self._.source}",
            "targetRefName": f"refs/heads/{self._.target}",
            "title": self._.title,
            "repositoryId": self._.repo_id
        }

        organization = ImportEnvKeyEnum.ORGANIZATION.value
        project_name = ImportEnvKeyEnum.PROJECT_NAME.value

        logger.info(f'Organization : {organization}')
        logger.info(f'Project : {project_name}')
        logger.info(f'header : {headers}')
        logger.info(f'body : {body}')

        result = requests.post(
            url=self.getURL(
                organization=organization,
                project=project_name
            ),
            headers=headers,
            data=json.dumps(body)
        )
        
        logger.debug(result.status_code)
        logger.debug(result.headers)
        logger.debug(result.json())

        result_json = result.json()
        pull_request_url = result_json['url']
        logger.info(f'Pull request url : {pull_request_url}')
        
        return pull_request_url

    def getURL(self, organization:str, project:str) -> str:
        return f'https://dev.azure.com/{organization}/{project}/_apis/pullrequest/pullrequests?api-version=7.1'

class PullRequestMergeController():
    
    def __init__(self ):
        pass