from flask import Flask
import logging

from views import webhook_blueprint
from config import Config
from ai_bot import AIBot


def create_app():
    #app set up function
    app = Flask(__name__)
    Config.configure_logging()
    
    app.register_blueprint(webhook_blueprint)
    
    #create a separate bot instance for each phone number,
    #this allows different users to have separate conversations with the chatbot
    #it also allows different users to use different google callendar APIs
    app.bot_instance = AIBot()
    
    return app



if __name__ == '__main__':
    app = create_app()
    
    logging.info('Flask app started')
    app.run(host='0.0.0.0', port=5000)
    
    
#running app:
#1) python3 main.py
#2) ngrok http 5000 --domain=light-goat-driving.ngrok-free.app  (expose to the web using ngrok)

    