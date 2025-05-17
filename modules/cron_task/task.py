#
import threading
from enum import Enum
from typing import Any

from search.grasp import crawl_data
from modules.models import Website, User
from .word_cutter import WordCutter


class UPDATE_TYPE(Enum):
    INCR = 0
    ALL = 1


def task(titles, _from, _to, ut=UPDATE_TYPE.INCR):
    user_ids = [user.id for user in User.objects.all()]

    def first_element(l: list) -> str:
        if len(l) >= 1:
            return l[0]

        return ""

    for title in titles[_from, _to + 1]:
        cutter = WordCutter(title)
        possible_keywords = cutter.cut()


        # 增量更新只在现有的基础上更新一个关键词
        # 全量更新则更新所有
        if ut == UPDATE_TYPE.INCR:
            w = first_element(possible_keywords)  # 一个关键词
            if w == '':
                continue

            for user_id in user_ids:
                crawl_data(w, user_id)

        elif ut == UPDATE_TYPE.ALL:
            for keyword in possible_keywords:  # 所有关键词

                if keyword == '':
                    continue

                for user_id in user_ids:
                    crawl_data(keyword, user_id)


def incremental_update():
    titles = get_titles()
    total_tasks = len(titles)
    pre_task_len = 10

    for running_task_point in range(0, total_tasks, pre_task_len):
        # 从每一个运行任务的节点开始到下一个节点结束
        threading.Thread(None, target=task, args=(titles, running_task_point, pre_task_len))


def complete_update():
    titles = get_titles()
    total_tasks = len(titles)
    pre_task_len = 10

    for running_task_point in range(0, total_tasks, pre_task_len):
        # 从每一个运行任务的节点开始到下一个节点结束
        threading.Thread(None, target=task, args=(titles, running_task_point, pre_task_len, UPDATE_TYPE.ALL))


def get_titles() -> Website[str]:
    websites = Website.objects.all()
    return [website.title for website in websites]
