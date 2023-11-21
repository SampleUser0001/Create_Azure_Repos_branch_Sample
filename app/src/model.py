from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from typing import List

@dataclass
class BranchModel():
    source: str
    feature: str
    target: str
    
@dataclass_json
@dataclass
class RepositoryModel():
    repo_name: str
    branches: List[BranchModel] = field(default_factory=list)
    
@dataclass
class CreatePullRequestModel():
    source: str
    target: str
    title: str
    required: List[str]
    optional: List[str]
    repo_id: str
    repo_name: str
    
    def __init__(
        self,
        repo_name:str,
        repo_id:str,
        branch: BranchModel,
        branch_date:str,
        pull_request_source_branch: str,
        requred: List[str],
        optional: List[str]):

        self.source = pull_request_source_branch
        self.target = branch.target
        self.title = f'{branch.source}({branch_date}) -> {branch.target}'
        self.repo_name = repo_name
        self.repo_id = repo_id
        self.required = requred
        self.optional = optional
        
# TODO データの持ち方は考える。
@dataclass
class ExportModel():
    repo_name:str
    source:str
    feature:str
    target:str
    pull_request_url:str