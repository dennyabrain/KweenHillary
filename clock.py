from apscheduler.schedulers.blocking import BlockingScheduler
from rq import Queue
from worker import conn
from HillaryBot import tweet

q = Queue(connection=conn)
sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=59)
def OneMinuteClock():
	print('this job runs every 59 minutes')
	result = q.enqueue(tweet)

sched.start()