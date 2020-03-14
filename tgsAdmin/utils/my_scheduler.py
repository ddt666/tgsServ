from apscheduler.schedulers.background import BackgroundScheduler
# from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
# jobstores = {
#     'default': RedisJobStore(jobs_key='dispatched_trips_jobs', run_times_key='dispatched_trips_running', host='localhost', port=6379)
# }
jobstores = {
    'redis': RedisJobStore(host='localhost', port=6379),
}
executors = {
    'default': ThreadPoolExecutor(10),
    'processpool': ProcessPoolExecutor(3)
}

scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors)
# scheduler.add_jobstore(jobstores, 'default')
# register_events(scheduler)
scheduler.start()
