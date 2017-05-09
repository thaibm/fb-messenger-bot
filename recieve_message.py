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

                    send_action(sender_id)
                    send_message(sender_id, message_text) # hàm này ko lặp
                    
                    list_book = knn(5, message_text)
                    # send_list(sender_id, list_book) # Dung ham nay se bị lặp

                    # book = BookRecord.get_by_name(message_text)
                    # send_book(sender_id, book)

                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get(
                        "postback"):  # user clicked/tapped "postback" button in earlier message
                    pass


def send_action(recipient_id):
    log("sending message to {recipient}: {text}".format(recipient=recipient_id,
                                                        text="sent action"))
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
        "sender_action": "typing_on",
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages",
                      params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
    log(r.text)


def send_message(recipient_id, message_text):
    log("sending message to {recipient}: {text}".format(recipient=recipient_id,
                                                        text=message_text))
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
    r = requests.post("https://graph.facebook.com/v2.6/me/messages",
                      params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
    log(r.text)


def send_book(recipient_id, book):
    log("sending message to {recipient}: {text}".format(recipient=recipient_id,
                                                        text=book.name))
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
            "text": book.name
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages",
                      params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
    log(r.text)


def send_list(recipient_id, list):
    log("sending message to {recipient}: {text}".format(recipient=recipient_id,
                                                        text="Sent list book"))
    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    book_1 = BookRecord.get(list[0][0]+1)
    book_2 = BookRecord.get(list[1][0]+1)
    book_3 = BookRecord.get(list[2][0]+1)
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "list",
                    "elements": [
                        {
                            "title": book_1.name,
                            "image_url": "https://d30y9cdsu7xlg0.cloudfront.net/png/1009-200.png",
                            "subtitle": book_1.author + "\n" + book_1.description,
                            # "default_action": {
                            #     "type": "web_url",
                            #     "url": "https://peterssendreceiveapp.ngrok.io/shop_collection",
                            #     # "messenger_extensions": true,
                            #     "webview_height_ratio": "tall",
                            #     "fallback_url": "https://peterssendreceiveapp.ngrok.io/"
                            # }
                        },
                        {
                            "title": book_2.name,
                            "image_url": "https://d30y9cdsu7xlg0.cloudfront.net/png/1009-200.png",
                            "subtitle": book_2.author,
                            # "default_action": {
                            #     "type": "web_url",
                            #     "url": "https://peterssendreceiveapp.ngrok.io/view?item=100",
                            #     # "messenger_extensions": true,
                            #     "webview_height_ratio": "tall",
                            #     "fallback_url": "https://peterssendreceiveapp.ngrok.io/"
                            # }
                        },
                        {
                            "title": book_3.name,
                            "image_url": "https://d30y9cdsu7xlg0.cloudfront.net/png/1009-200.png",
                            "subtitle": book_3.author,
                            # "default_action": {
                            #     "type": "web_url",
                            #     "url": "https://peterssendreceiveapp.ngrok.io/view?item=101",
                            #     # "messenger_extensions": true,
                            #     "webview_height_ratio": "tall",
                            #     "fallback_url": "https://peterssendreceiveapp.ngrok.io/"
                            # }
                        }
                    ]
                }
            }
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages",
                      params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
    log(r.text)


def log(message):  # simple wrapper for logging to stdout on heroku
    print(str(message))
    sys.stdout.flush()
