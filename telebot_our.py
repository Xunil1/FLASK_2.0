import telebot as tb

bot = tb.TeleBot("2050823409:AAFHYUHk0lvFPJNCRr-B3aHlqaFEjMr-vQE")


@bot.message_handler(commands = ['start'])
def start(message):

    bot.send_message(message.chat.id, 'Приветствую.')
    chat_id = message.chat.id
    file = open("id.txt", "w")
    file.write(str(chat_id))
    file.close()


def send_message(turple_order):
    file = open("id.txt", "r")
    chat_id = file.read()
    file.close()
    message = "Номер заказа: " + str(turple_order["id"]) + "\nИмя: " + str(turple_order["name"]) + "\nТелефон: " + str(turple_order["phone"]) + "\nАдрес: " + str(turple_order["address"]) + "\nID товара: "   + str(turple_order["product_id"]) + "\nНазвание товара: " + str(turple_order["product_name"]) + "\nЦена товара: " + str(turple_order["product_price"])  + " ₽"
    bot.send_message(int(chat_id), message)


#bot.polling(none_stop=True)