from bot import Bot
from apscheduler.schedulers.blocking import BlockingScheduler
from configuration import FREQUENCY

scheduler = BlockingScheduler()


@scheduler.scheduled_job('interval', hours=FREQUENCY)
def timed_run():

    bot = Bot()
    bot.run()


if __name__ == '__main__':

    scheduler.start()
