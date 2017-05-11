# # coding: utf8
# from send import send_thread
# import json
#
#
# def send_persistent_menu():
#     data = json.dumps({
#         "setting_type": "call_to_actions",
#         "thread_state": "existing_thread",
#         "call_to_actions": [
#             {
#                 "type": "postback",
#                 "title": "Tìm kiếm chính xác",
#                 "payload": "DEFAULT_SEARCH"
#             },
#             {
#                 "type": "postback",
#                 "title": "Tìm kiếm nâng cao",
#                 "payload": "ADVANCED_SEARCH"
#             }
#         ]
#     })
#     send_thread(data)
