from bot import Bot

def main():

    bot = Bot()

    while True:

        if bot.isAcessTokenExpired():

            bot.refreshAccessToken()




if __name__ == '__main__':
    main()
