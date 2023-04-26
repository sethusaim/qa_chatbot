import os

from langchain.callbacks import get_openai_callback
from langchain.chains.llm import LLMChain
from telebot import TeleBot

from src.api.chain import BotChain
from src.logger import logging

bot = TeleBot(os.environ["API_KEY"])

llm_chain: LLMChain = BotChain()


@bot.message_handler(commands=["start"])
def send_welcome(message):
    """
    This function sends a welcome message to the user introducing a question answering bot.

    Args:
      message: The message object that contains information about the incoming message, such as the chat
    ID and the text of the message. This function sends a welcome message to the user when they first
    interact with the bot.
    """
    bot.send_message(
        message.chat.id,
        "Hello! I'm a question answering bot powered by OpenAI and built by Sethu Sai M. Send me a question and I'll do my best to answer it!",
    )


@bot.message_handler(commands=["help"])
def help(message):
    """
    This function sends a message listing the supported commands to the user.

    Args:
      message: The message parameter is the message object that contains information about the message
    sent by the user, such as the chat ID, message text, and sender information.
    """
    bot.reply_to(
        message,
        "I support the following commands: \n /start \n /info \n /help \n /status",
    )


@bot.message_handler(commands=["info"])
def info(message):
    """
    The function sends a message to the user with information about the Telegram bot.

    Args:
      message: The message parameter is the message object that is received by the bot from the user. It
    contains information such as the chat ID, message ID, sender information, and the actual text of the
    message.
    """
    bot.reply_to(
        message,
        "I am a simple Telegram bot created by Sethu Sai M for iNeuron.",
    )


@bot.message_handler(commands=["status"])
def status(message):
    """
    This function sends a reply message stating that the bot is up and running.

    Args:
      message: The message object that the bot receives from the user. It contains information such as
    the user's chat ID, the text of the message, and any other relevant data.
    """
    bot.reply_to(message, "I am up and running.")


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    """
    This function handles incoming messages, generates a response using a language model, and sends the
    response back to the user.

    Args:
      message: The message object contains information about the incoming message, such as the text,
    sender, and chat ID.
    """
    user_message: str = message.text

    with get_openai_callback() as cb:
        bot_response = llm_chain.predict(human_input=user_message)

        logging.info(f"Cost is {cb}")

        bot.send_message(message.chat.id, bot_response)


print("Hey, I am up....")

bot.polling()
