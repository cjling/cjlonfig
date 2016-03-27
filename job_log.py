#!/usr/bin/env python
# encoding: utf-8

from anydo_api.client import Client
from anydo_api.task import Task
from datetime import datetime
import time
import os
from geeknote.geeknote import Notes


def get_today_title():
    now_date = datetime.today()
    return "%d/%d/%d" %(now_date.year, now_date.month, now_date.day)


def save_log(user, tasks):
    log = ""
    index = 1
    # gap = ".\n.\n"
    gap = "\n\n"

    for task in tasks:
        if task['status'] == "CHECKED":
            continue
        log += "#%d.%s\n" %(index, task['title'])
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

    # log_task = Task.create(user=user, title=get_today_title(), priority="Normal", repeatingMethod='TASK_REPEAT_OFF')
    # log_task.add_note(log)
    # cmd = "geeknote create --title %s --context %s --notebook \"98_工作日志\"" %(get_today_title(), log)
    # os.system(cmd)

    print "will cache temp log"
    f = open("./temp.log", "w")
    f.write(log)
    f.close()
    Notes().create(title=get_today_title(), content="./temp.log", notebook="98_工作日志")
    print "save log sucessfully!"


def is_doing(due_date):
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


def start():
    user = Client(email='cjling@aliyun.com', password='916sa...').get_user()
    cate = [cate for cate in user.categories() if cate['name'] == u"工作"]

    if len(cate) != 1:
        return

    works = cate[0].tasks()
    tasks = []
    for work in works:
        if work['dueDate'] is None:
            continue
        due_date = datetime.fromtimestamp(work['dueDate'] / 1000)
        if is_doing(due_date):
            tasks.append(work)

    save_log(user, tasks)


def start_wrapper():
    try:
        start()
        return True
    except Exception, e:
        print "something wrong happened try ag after 4 second:"
        print e
        time.sleep(4)
        return False


if __name__ == '__main__':
    flag = False
    while not flag:
        flag = start_wrapper()