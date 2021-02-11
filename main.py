from bot import Bot
from apscheduler.schedulers.blocking import BlockingScheduler

scheduler = BlockingScheduler()


@scheduler.scheduled_job('interval', hours=6)
def timed_run():

    bot = Bot()
    bot.run()


if __name__ == '__main__':

    # scheduler.start()
    bot = Bot()
    bot.force_run()
