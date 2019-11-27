from rasa_core_sdk import Action
from pymongo import MongoClient
import re

class ActionSalvarDataAtv(Action):
    def name(self):
        return "action_salvarDataAtv"

    def run(self, dispatcher, tracker, domain):
        try:
            tracker = tracker.current_state()

            sender_id = tracker['sender_id']
            client = MongoClient("mongo:27017")
            db = client.telegramdb
            collectionsUsers = db.user

            Name = collectionsUsers.find_one({'SenderID': sender_id})['first_name']
            Data2Save = tracker['latest_message']['text']

            TituloSaved = collectionsUsers.find_one({'SenderID': sender_id})['VTitulo']

            if(re.match(r"^(?:(?:31(\/|-|\.)(?:0?[13578]|1[02]))\1|(?:(?:29|30)(\/|-|\.)(?:0?[13-9]|1[0-2])\2))(?:(?:1[6-9]|[2-9]\d)?\d{2})$|^(?:29(\/|-|\.)0?2\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00))))$|^(?:0?[1-9]|1\d|2[0-8])(\/|-|\.)(?:(?:0?[1-9])|(?:1[0-2]))\4(?:(?:1[6-9]|[2-9]\d)?\d{2})$", Data2Save)):
                collectionsUsers.update_one({'SenderID': sender_id}, {'$set': {'VData': Data2Save}})
                dispatcher.utter_message("Ok")
                dispatcher.utter_message(Name + ", agora me manda o que devo modificar.")
            else:
                activities = collectionsUsers.find_one({'SenderID': sender_id})['activities']
                for data in activities:
                    if(data['TituloDaAtv'] == TituloSaved):
                        collectionsUsers.update_one({'SenderID': sender_id}, {'$set': {'VData': data['Data']}})
            client.close
        except ValueError:
            dispatcher.utter_message(ValueError)
