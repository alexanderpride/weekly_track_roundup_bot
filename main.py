from bot import Bot
from time import sleep


def main():

    bot = Bot()

    print(bot.spotipy_auth_manager.get_authorize_url())
    code = bot.spotipy_auth_manager.parse_response_code(input("Enter the URL: "))
    bot.spotipy_auth_manager.get_access_token(code)

    while True:

        if bot.isAcessTokenExpired():

            bot.refreshAccessToken()

        if bot.isNewVideo():

            bot.run()

        sleep(10)




if __name__ == '__main__':
    main()
