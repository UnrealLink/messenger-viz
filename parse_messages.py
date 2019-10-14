import os
import time
import json
import matplotlib.pyplot as plt
import matplotlib
from datetime import datetime, timedelta
from message import Message

ME = "John Doe"
DATA_PATH = "D:\\Ressources\\Data\\Facebook2\\messages\\inbox"
MESSAGE_FILE = "message_1.json"


def parse_message(message):
    if message.get('content'):
        return Message(message['content'], message['sender_name'], 
                       datetime.fromtimestamp(message['timestamp_ms']/1000))
    return None

def parse_messages(file):
    messages = []

    with open(file, 'r', encoding='utf8') as f:
        data = json.load(f)
    for message in data['messages']:
        parsed_message = parse_message(message)
        if parsed_message:
            messages.append(parsed_message)
    participants = [elm['name'] for elm in data['participants'] if elm['name'] != ME]

    return {'participants': participants, 'messages': messages}

def parse_all_messages(name=ME, dir=DATA_PATH, message_file=MESSAGE_FILE, no_groups=True):
    all_messages = {}
    t = time.time()
    for d in os.listdir(dir):
        res = parse_messages(f"{dir}\\{d}\\{message_file}")
        if len(res['participants']) == 1:
            all_messages[res['participants'][0]] = res['messages']
    print(f"Parsed all messages in {time.time()-t}s.")
    return all_messages


def get_values(messages, dates):
    nb_messages = [0]*len(dates)
    i = 0
    for message in messages:
        placed = False
        while i < len(dates) and not placed:
            if message.date >= dates[i]:
                nb_messages[i] += 1
                placed = True
            else:
                i += 1
    return nb_messages

def show_evolution(convos, max_date=datetime(2019, 10, 9), 
                   min_date=datetime(2014, 9, 1), 
                   bin=timedelta(days=7)):
    date = max_date
    dates = []
    while date > min_date:
        dates.append(date)
        date -= bin
    coords = matplotlib.dates.date2num(dates)
    for (name, messages) in convos:
        values = get_values(messages, dates)
        plt.plot_date(coords, values, '-', label=name)
    plt.legend()
    plt.show()

def parse_and_show_messages(name, data_path, min_date, max_date, bin, min_rank, max_rank):
    messages = parse_all_messages(name, data_path)
    sorted_messages = sorted(messages.items(), key=lambda x : len(x[1]), reverse=True)
    show_evolution(sorted_messages[int(min_rank):int(max_rank)], 
                   datetime(*list(map(int, max_date.split('/')))),
                   datetime(*list(map(int, min_date.split('/')))),
                   timedelta(days=int(bin)))
