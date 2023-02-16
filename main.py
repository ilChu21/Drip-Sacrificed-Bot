from burnFuncs import *
import os, telebot, time

bot = telebot.TeleBot(os.environ["TELEGRAM_DRIP_SACRIFICED_API_KEY"])
print('SACRIFICED bot active.')


@bot.message_handler(commands=['start', 'help'])
def start(msg):
    bot.reply_to(msg,
        f"Hi @{msg.from_user.username}! Post a public address to get it's Drip sacrificed results.")


@bot.message_handler(content_types=['text'])
def sacrificed(msg):
        if msg.text.startswith('0x'):
            try:
                address = web3.toChecksumAddress(msg.text)
                userBurnDetails = getTotalBurns(address)
                nl = '\n'
                bot.reply_to(msg,
                    f"*{address[:6]}...{address[-4:]}*\n\n"
                    f"Total DRIP Sacrificed:\n*🔥 {round(userBurnDetails['totalBurned'], 3):,} 🔥*\n\n"
                    f"History ({userBurnDetails['burnCount']:,}):\n{f'{nl}'.join(userBurnDetails['burnTxs'])}",
                    parse_mode='Markdown',
                    disable_web_page_preview=True)
            except:
                bot.reply_to(msg,
                    "Not a valid BSC address, or issue with API. Please try again.")


while True:
    try:
        bot.polling()
    except Exception:
        time.sleep(15)