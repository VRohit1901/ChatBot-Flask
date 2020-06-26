from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from requests import get
from bs4 import BeautifulSoup
import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

bot= ChatBot('Jarvis')

trainer = ListTrainer(bot)

for file in os.listdir('C:/Users/Anonymous/Desktop/ChatBot/data/'):

    chats = open('C:/Users/Anonymous/Desktop/ChatBot/data/' + file, 'r').readlines()

    trainer.train(chats)

@app.route("/")
def hello():
    return render_template('chat.html')

@app.route("/ask", methods=['POST'])
def ask():

    message = str(request.form['messageText'])

    bot_response = bot.get_response(message)

    while True:

        if bot_response.confidence > 0.1:

            bot_response = str(bot_response)      
            print(bot_response)
            return jsonify({'status':'OK','answer':bot_response})
 
        elif message == ("bye"):

            bot_response='Hope to see you soon'

            print(bot_response)
            return jsonify({'status':'OK','answer':bot_response})

            break

        else:
        
            try:
                url  = "https://en.wikipedia.org/wiki/"+ message
                page = get(url).text
                soup = BeautifulSoup(page,"lxml")
                p    = soup.find_all("p")
                return jsonify({'status':'OK','answer':p[1].text})

            except IndexError as error:

                bot_response = 'Sorry i have no idea about that.'
            
                print(bot_response)
                return jsonify({'status':'OK','answer':bot_response})

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)