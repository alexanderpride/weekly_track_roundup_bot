from bot import Bot
from apscheduler.schedulers.blocking import BlockingScheduler

scheduler = BlockingScheduler()


def init_run():

    bot = Bot()
    bot.force_run()


@scheduler.scheduled_job('interval', hours=6)
def timed_run():

    bot = Bot()
    bot.run()


if __name__ == '__main__':

    init_run()
    scheduler.start()

