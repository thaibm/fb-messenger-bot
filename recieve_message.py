# coding: utf8
import os
import sys
import json

import requests
from flask import Flask, request
from database import db, Book
from models.book import BookRecord
from wmd.wmd import knn

def recieve(data):

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # someone sent us a message

                    sender_id = messaging_event["sender"][
                        "id"]  # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"][
                        "id"]  # the recipient's ID, which should be your page's facebook ID
                    message_text = messaging_event["message"][
                        "text"]  # the message's text

                    k_doc = knn(5, message_text)
                    book = BookRecord.get(k_doc[0][0] +1)
                    book1 = BookRecord.get(k_doc[1][0]+1)
                    book2 = BookRecord.get(k_doc[2][0]+1)
                    book3 = BookRecord.get(k_doc[3][0]+1)
                    book4 = BookRecord.get(k_doc[4][0]+1)
                    # book = BookRecord.get(50)
                    send_message(sender_id, book.name)
                    send_message(sender_id, book1.name)
                    send_message(sender_id, book2.name)
                    send_message(sender_id, book3.name)
                    send_message(sender_id, book4.name)

                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get(
                        "postback"):  # user clicked/tapped "postback" button in earlier message
                    pass


def send_message(recipient_id, message_text):

    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))
    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)

def log(message):  # simple wrapper for logging to stdout on heroku
    print(str(message))
    sys.stdout.flush()
