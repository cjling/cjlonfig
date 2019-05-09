#!/usr/bin/env python
# encoding: utf-8

from datetime import datetime
import time
import os

import logging
from logging.handlers import RotatingFileHandler

from geeknote.geeknote import Notes
from anydo_api.client import Client

# formatter = logging.Formatter('%(asctime)s %(filename)s[%(lineno)d] %(levelname)s: %(message)s')
rfh = RotatingFileHandler('/home/cjling/data/job.log', maxBytes=5*1024*1024*1024,backupCount=5)
rfh.setLevel(logging.DEBUG)
# rfh.setFormatter(formatter)

LOG = logging.getLogger("job_logger")
LOG.setLevel(logging.DEBUG)
LOG.addHandler(rfh)

def get_today_title():
    now_date = datetime.today()
    return "%d/%d/%d" %(now_date.year, now_date.month, now_date.day)

def is_work_doing(due_date):
    now_date = datetime.today()
    if due_date.year < now_date.year:
        return True
    elif due_date.year > now_date.year:
        return False

    if due_date.month < now_date.month:
        return True
    elif due_date.month > now_date.month:
        return False

    if due_date.day <= now_date.day:
        return True
    else:
        return False

def get_job_log(tasks):
    log = ""
    index = 1
    gap = "\n\n"

    for task in tasks:
        if task['status'] == "CHECKED":
            continue
        log += "%d.%s\n" %(index, task['title'])
        index += 1
        if len(task.notes()) != 0:
            log += "--Note:\n"
            for note in task.notes():
                log += "%s\n" %note

        subtask_list = [subtask for subtask in task['subTasks'] if subtask['status'] != "CHECKED"]
        if len(subtask_list) != 0:
            log += "--Subtasks:\n"
            sub_index = 1
            for sub in subtask_list:
                log += "%d)%s\n" %(sub_index, sub['title'])
                sub_index += 1
        log += gap

    if log[-2:] == gap:
        log = log[:-2]
    return log

def get_anydo_user():
    passwd=os.popen("anydo_passwd").read()
    user = Client(email='cjling@aliyun.com', password=passwd).get_user()
    return user

def get_job_tasks(user):
    cate = [cate for cate in user.categories() if cate['name'] == u"工作"]

    if len(cate) != 1:
        return

    works = cate[0].tasks()
    tasks = []
    for work in works:
        if work['dueDate'] is None:
            continue
        due_date = datetime.fromtimestamp(work['dueDate'] / 1000)
        if is_work_doing(due_date):
            tasks.append(work)
    return tasks

def get_job_log_from_anydo():
    user_cjling = get_anydo_user()
    job_tasks = get_job_tasks(user_cjling)
    job_log = get_job_log(job_tasks).encode('utf-8')
    return job_log

def save_job_log_to_yxbj(log):
    Notes().create(title=get_today_title(), content=log, notebook="98_工志")

def save_job_log_to_yxbj(log):
    Notes().create(title=get_today_title(), content=log, notebook="98_工志")

if __name__ == '__main__':
    try:
        job_log = get_job_log_from_anydo()
        LOG.info("%s\n%s\n%s"%("*************************************************************************************************************************************", get_today_title(), job_log.decode('utf8').encode('gbk')))
        # save_job_log_to_yxbj(job_log)
    except Exception as e:
        LOG.info(e)
