import sys

from src.bot.telegram import bot
from src.exception import CustomException


def run_bot():
    """
    This function runs a bot and raises a custom exception if an error occurs.
    """
    try:
        bot.polling()

    except Exception as e:
        raise CustomException(e, sys)


if __name__ == "__main__":
    run_bot()
