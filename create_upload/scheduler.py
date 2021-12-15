from apscheduler.schedulers.background import BackgroundScheduler
from create_upload.create import create_upload
from create_upload.send_upload import send


def x():
    create_upload(300*60)
    send()


scheduler = BackgroundScheduler()

#scheduler.add_job(x, 'cron', minute = 0)
#scheduler.add_job(x, 'cron', minute = 30)
