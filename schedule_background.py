import concurrent.futures
import threading
import time
import logging
from db.db import reset_post_count

import schedule


def run_continuously(interval=60):
    cease_continuous_run = threading.Event()

    # TODO: подумать над вынесением из функции
    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                schedule.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.start()
    return cease_continuous_run


def update_users_sugg_count():
    reset_post_count()
    logging.info('Posts count updated')


schedule.every().friday.do(update_users_sugg_count)
