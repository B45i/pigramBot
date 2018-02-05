import RPi.GPIO as GPIO
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

# Telegram token
TOKEN = 'your telegram token'

pins = ('pin1', 'pin2', 'pin3', 'pin4', 'pin5', 'pin6')

# change to names the devices you want to control
devices = {
    'pin1': 'Living room light',
    'pin2': 'Bedroom light',
    'pin3': 'TV',
    'pin4': 'Bedroom Fan',
    'pin5': 'AC',
    'pin6': 'Hall light',
}

# Everything is turned off at the beginning
pin_status = {}
for pin in pins:
    pin_status[pin] = False

# Using GPIOs 33, 35, 36, 37, 38, 49. you can change the pins if you want
gpios = {
    'pin1': 33,
    'pin2': 35,
    'pin3': 36,
    'pin4': 37,
    'pin5': 38,
    'pin6': 40,
}


def start(bot, update):
    options = {}
    for pin in pins:
        if pin_status[pin]:
            options[pin] = 'Turn off %s' % devices[pin]
        else:
            options[pin] = 'Turn on %s' % devices[pin]

    keyboard = [[InlineKeyboardButton(options['pin1'], callback_data='1'),
                 InlineKeyboardButton(options['pin2'], callback_data='2')],

                [InlineKeyboardButton(options['pin3'], callback_data='3'),
                 InlineKeyboardButton(options['pin4'], callback_data='4')],

                [InlineKeyboardButton(options['pin5'], callback_data='5'),
                 InlineKeyboardButton(options['pin6'], callback_data='6')],

                [InlineKeyboardButton('Turn on everything', callback_data='7')],
                [InlineKeyboardButton('Turn off everything', callback_data='8')]]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please choose:', reply_markup=reply_markup)


def toggle_pin(switched_pin):
    pin_status[switched_pin] = not pin_status[switched_pin]
    GPIO.output(gpios[switched_pin], pin_status[switched_pin])
    if pin_status[switched_pin]:
        return '%s Turned on successfully ' % devices[switched_pin]
    else:
        return '%s Turned off successfully ' % devices[switched_pin]


def button(bot, update):
    replay = ""
    query = update.callback_query
    if query.data == '1':
        replay = toggle_pin('pin1')
    elif query.data == '2':
        replay = toggle_pin('pin2')
    elif query.data == '3':
        replay = toggle_pin('pin3')
    elif query.data == '4':
        replay = toggle_pin('pin4')
    elif query.data == '5':
        replay = toggle_pin('pin5')
    elif query.data == '6':
        replay = toggle_pin('pin6')
    elif query.data == '7':
        for pin in pins:
            pin_status[pin] = True
            GPIO.output(gpios[pin], True)
        replay = 'All devices turned on successfully'
    elif query.data == '8':
        for pin in pins:
            pin_status[pin] = False
            GPIO.output(gpios[pin], False)
        replay = 'All devices turned off successfully'

    bot.edit_message_text(text=replay,
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id)


def setup():
    GPIO.setmode(GPIO.BOARD)
    for pin in gpios:
        GPIO.setup(gpios[pin], GPIO.OUT)


def main():
    setup()

    updater = Updater(TOKEN)
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))

    updater.start_polling()
    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()

if __name__ == '__main__':
    main()
