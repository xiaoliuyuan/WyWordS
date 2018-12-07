'''
    定义这个app的所有celery任务
'''

import time

# 任务模块
from celery import task

# celery任务task
@task
def show():
    print('hello')
    time.sleep(5)
    print('world')