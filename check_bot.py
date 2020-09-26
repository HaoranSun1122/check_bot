import telepot
import requests
from bs4 import BeautifulSoup
import time
from telepot.loop import MessageLoop

chat_id_list = [224562648,]

bot = telepot.Bot('441503260:AAE2HNhWroVQHDEzkmBpT7REvtXI4PBfu7s')

list_link_all = ["https://www.unieuro.it/online/Playstation-5/PlayStation-5-Digital-Edition-pidSONPS5DIGITAL","https://www.unieuro.it/online/Playstation-5/PlayStation-5-pidSONPS5DISC",
                "https://www.trony.it/online/console-giochi-e-tempo-libero/console/play-station-5/sony-ent-playstation-5_sku-2200010367", "https://www.euronics.it/console/sony-computer/playstation-5-digital-edition/eProd202008907/",]

list_link = ["https://www.unieuro.it/online/Playstation-5/PlayStation-5-Digital-Edition-pidSONPS5DIGITAL",]

is_avable = False



def find_ps5(list_link):

    global is_avable

    if (is_avable == False):

        for link_ in list_link:

            page = requests.get(link_, headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.15',})
            soup = BeautifulSoup(page.content, 'html.parser')

            if (soup.findAll("div", {"class": "available on susy--span-4"}) or soup.find(id="disponibile") or soup.findAll("span", {"class": "button__icon--iconTxt i-prenota_ritira"}) or soup.findAll("span", {"class": "button__icon--iconTxt i-cart"})):

                is_avable = True
                for chat_id in chat_id_list:
                    bot.sendMessage(chat_id, "!!! PS5 DISPONIBILE !!!")
                    bot.sendMessage(chat_id, "IL LINK DI PREORDINE E':")
                    bot.sendMessage(chat_id, link_)
                    print("!!! PS5 DISPONIBILE !!!")
                    print(link_)
                    continue

            elif (soup.findAll("div", {"class": "available off susy--span-4"}) or soup.find(id="nondisponibile") or soup.findAll("span", {"class": "button__icon--iconTxt i-notifica"})):

                #print("PS5 NON DISPONIBILE")
                #for chat_id in chat_id_list:
                    #bot.sendMessage(chat_id, "PS5 NON DISPONIBILE")
                continue

            else:

                is_avable = True
                for chat_id in chat_id_list:
                    bot.sendMessage(chat_id,"!!! PROBLEMA BOT PS5 !!!")
                    print("!!! PROBLEMA BOT PS5 !!!")
                    print(link_)
                    continue


def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']
    sender = msg['from']['id']

    print('Got command: %s' % command)

    if sender in chat_id_list :

        if command == '/True':

            kill = True
            bot.sendMessage(chat_id, 'Attivato')

        elif command == '/False':

            kill = False
            bot.sendMessage(chat_id, 'Disattivato')

        elif command == '/riavvia':

            bot.sendMessage(chat_id, 'Riavvio in corso signore...')
            os.system("sudo reboot")
            bot.sendMessage(chat_id, 'Riavvio completato')

        elif command == '/spegni':

            bot.sendMessage(chat_id, 'Spegnimento in corso signore...')
            os.system("sudo shutdown -h now")

        elif command == '/ps5':

            find_ps5(list_link)

            if (is_avable == False):

                bot.sendMessage(chat_id, 'Mi dispiace, ma non è ancora disponibile in nessun negozio.')


    elif sender not in chat_id_list:
      bot.sendMessage(224562648, chat_id)
      bot.sendMessage(chat_id, 'Accesso negato')


MessageLoop(bot, handle).run_as_thread()
print('I am listening ...')


while 1:

    MessageLoop(bot, find_ps5(list_link))
    time.sleep(90)

    if (is_avable == True):

        time.sleep(300)
        is_avable = False
