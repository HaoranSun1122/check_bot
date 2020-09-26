import telepot
import requests
from bs4 import BeautifulSoup
import time
from telepot.loop import MessageLoop

#Replace YOUR _CHAD_ID with your chat id code
chat_id_list = [YOUR_CHAD_ID,]

bot = telepot.Bot('TOKEN')

#Insert all product link you want to check
list_link = ["first_link","second_link","third_link", "fourth_link",]


is_avable = False


def find_product(list_link):

    global is_avable

    if (is_avable == False):

        for link_ in list_link:

            page = requests.get(link_, headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.15',})
            soup = BeautifulSoup(page.content, 'html.parser')

            if (soup.findAll("div", {"class": "available on susy--span-4"}) or soup.find(id="disponibile") or soup.findAll("span", {"class": "button__icon--iconTxt i-prenota_ritira"}) or soup.findAll("span", {"class": "button__icon--iconTxt i-cart"})):

                is_avable = True
                for chat_id in chat_id_list:
                    bot.sendMessage(chat_id, "!!! AVABLE !!!")
                    bot.sendMessage(chat_id, "THE LINK IS:")
                    bot.sendMessage(chat_id, link_)
                    print("!!! AVABLE !!!")
                    print(link_)
                    continue

            elif (soup.findAll("div", {"class": "available off susy--span-4"}) or soup.find(id="nondisponibile") or soup.findAll("span", {"class": "button__icon--iconTxt i-notifica"})):

                continue

            else:

                is_avable = True
                for chat_id in chat_id_list:
                    bot.sendMessage(chat_id,"!!! PROBLEM, CHECK THE BOT !!!")
                    print("!!! PROBLEM, CHECK THE BOT !!!")
                    print(link_)
                    continue


def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']
    sender = msg['from']['id']

    print('Got command: %s' % command)

    if sender in chat_id_list :
      
      if command == '/is_avable':
        
        find_product(list_link)
        
          if (is_avable == False):
            
            bot.sendMessage(chat_id, 'Not avable yet.')


    elif sender not in chat_id_list:
      
      #Replace YOUR _CHAD_ID with your chat id code
      bot.sendMessage(YOUR_CHAD_ID, chat_id)
      bot.sendMessage(chat_id, 'You don\'t have the permission')


MessageLoop(bot, handle).run_as_thread()
print('I am listening ...')


while 1:

    MessageLoop(bot, find_product(list_link))
    time.sleep(90)

    if (is_avable == True):

        time.sleep(300)
        is_avable = False
