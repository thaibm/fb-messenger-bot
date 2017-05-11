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

                    if "text" in messaging_event["message"]:
                        message_text = messaging_event["message"][
                            "text"]  # the message's text

                        send_action(sender_id)

                        k = 3
                        send_list(sender_id, message_text, k)

                    else:
                        send_message(sender_id,
                                     "Hãy nhập thông sách bạn muốn tìm!")

                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):
                    # user clicked/tapped "postback" button in earlier message
                    payload = messaging_event["postback"]["payload"]
                    sender_id = messaging_event["sender"]["id"]
                    data = payload.split(";")
                    send_list(sender_id, data[1], int(data[0]))
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


def send_list(recipient_id, message_text, k):
    log("sending message to {recipient}: {text}".format(recipient=recipient_id,
                                                        text="Sent list book"))
    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }

    list_book = knn(k, message_text)

    if len(list_book) != 0:
        books = []
        for i in range(0, k):
            books.append(BookRecord.get(list_book[i][0] + 1))

        elements = [{
            "title": "Sách Việt",
            "image_url": "https://static.pexels.com/photos/213/blur-old-antique-book.jpg",
            "subtitle": "Chia sẻ thành công, Kết nối tri thức và nâng cao giá trị tinh thần cho cuộc sống!",
            "default_action": {
                "type": "web_url",
                "url": "https://www.facebook.com/S%C3%A1ch-Vi%E1%BB%87t-1483632485043890/?ref=aymt_homepage_panel",
                "webview_height_ratio": "tall",
            }
        }]
        for book in books[k - 3:k]:
            e = {
                "title": book.name,
                "image_url": "http://www.impostorsyndrome.com/wp-content/uploads/2012/06/openbook.png",
                "subtitle": book.author + "\n" + book.description,
                "default_action": {
                    "type": "web_url",
                    "url": book.url,
                    "webview_height_ratio": "tall",
                },
                "buttons": [
                    {
                        "title": "Xem",
                        "type": "web_url",
                        "url": book.url,
                        "webview_height_ratio": "tall",
                    }
                ]
            }
            elements.append(e)

        data = json.dumps({
            "recipient": {
                "id": recipient_id
            },
            "message": {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "list",
                        "top_element_style": "large",
                        "elements": elements,
                        "buttons": [
                            {
                                "title": "Xem thêm",
                                "type": "postback",
                                "payload": str(k+3)+";"+message_text,

                            }
                        ]
                    }
                }
            }
        })
    else:
        data = json.dumps({
            "recipient": {
                "id": recipient_id
            },
            "message": {
                "text": "Hãy nhập thông sách bạn muốn tìm!"
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
