import datetime

messages=[
    (1, 1, 1, "Salom", datetime.datetime(2024, 9, 20, 12, 56, 26)),
    (2, 1, 1, "nima", datetime.datetime(2024, 9, 20, 12, 56, 59)),
    (3, 1, 2, "Nima gap?", datetime.datetime(2024, 9, 20, 12, 58, 51)),
    (4, 1, 1, "321", datetime.datetime(2024, 9, 20, 12, 58, 58)),
    (5, 1, 1, "NIma nima gap?", datetime.datetime(2024, 9, 20, 12, 59, 5)),
]
for message in messages:
    idd,chat_id,sender_id, message_text, sent_time = message[:5] 
    print(f"{idd}  -   {chat_id}   -   {sender_id}   -   {message_text}    -    {sent_time}")
