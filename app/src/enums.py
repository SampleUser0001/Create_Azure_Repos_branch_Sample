# -*- coding: utf-8 -*-
from enum import Enum
import os

PYTHON_APP_HOME = os.getenv('PYTHON_APP_HOME')
SH_HOME = os.path.join(PYTHON_APP_HOME, 'sh')
class GitShEnum(Enum):
    CLONE=('git_clone.sh')
    DIFF=('git_diff.sh')
    CHECKOUT_FEATURE=('git_checkout_feature.sh')
    
    def __init__(self, file:str):
        self.path = os.path.join(SH_HOME, file)