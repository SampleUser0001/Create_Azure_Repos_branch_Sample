# -*- coding: utf-8 -*-
import json
import os

class LogUtil:
  
  @classmethod
  def get_log_conf(cls, log_conf_path):
    """ ログ設定ファイルを読み込む
    """
    with open(log_conf_path, mode='r') as f:
      log_conf = json.loads(f.read())
      log_conf['handlers']['fileHandler']['filename'] = os.getenv('PYTHON_APP_HOME') + '/' + log_conf['handlers']['fileHandler']['filename']
    return log_conf
