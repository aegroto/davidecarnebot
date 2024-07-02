import asyncio
import string
import random
import logging
import yaml

from telegram.ext import filters,  ApplicationBuilder, CommandHandler, MessageHandler

def load_config():
    return yaml.safe_load(open("config/settings.yaml"))

def main():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

    config = load_config()

    application = ApplicationBuilder().token(config["token"]).build()

    message_handler = MessageHandler(filters.TEXT  & (~filters.COMMAND), message_parse_handler)
    application.add_handler(message_handler)

    principessa_handler = CommandHandler('principessa', principessa_cmd_handler)
    application.add_handler(principessa_handler)

    ddh_handler = CommandHandler('ddh', ddh_cmd_handler)
    application.add_handler(ddh_handler)

    donzelli_handler = CommandHandler('donzelli', donzelli_cmd_handler)
    application.add_handler(donzelli_handler)

    donzelle_handler = CommandHandler('donzelle', donzelle_cmd_handler)
    application.add_handler(donzelle_handler)

    application.run_polling()

async def principessa_cmd_handler(update, context):
    await context.bot.sendMessage(chat_id=update.message.chat_id, text="Ma sei una principessa!")

async def ddh_cmd_handler(update, context):
    await context.bot.sendMessage(chat_id=update.message.chat_id, text="Ddddddddhhh!")

async def donzelli_cmd_handler(update, context):
    await context.bot.sendMessage(chat_id=update.message.chat_id, text="Non conquistare troppi donzelli")

async def donzelle_cmd_handler(update, context):
    await context.bot.sendMessage(chat_id=update.message.chat_id, text="Non conquistare troppe donzelle")

async  def message_parse_handler(update, _):
    reply = get_message_reply(update.message.text)
    if reply is not None:
        await update.message.reply_text(reply, reply_to_message_id=update.message.message_id, parse_mode="markdown")

def get_message_reply(msg_text):
    msg_text.translate(string.punctuation)
    msg_symbols = msg_text.split()

    config = load_config()
    message_triggers = config["message_triggers"]
    trigger_replies = config["trigger_replies"]

    for symbol in msg_symbols:
        for trigger_id in message_triggers:
            for trigger_symbol in message_triggers[trigger_id]:
                if symbol.lower() == trigger_symbol:
                    return random.choice(trigger_replies[trigger_id])

    if(random.uniform(0.0, 1.0) > (1.0 - config["random_reply_chance"])):
        return random.choice(trigger_replies["random"])

    return None

if __name__ == '__main__':
    main()
