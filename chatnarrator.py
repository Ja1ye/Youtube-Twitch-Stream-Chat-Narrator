import PySimpleGUI as sg
import time
from pytchat import LiveChat
import pyttsx3
from twitchobserver import Observer

layout = [  [sg.Text('Enter Stream URL (youtube or twitch)')],
            [sg.InputText(key='streamid')],
            [sg.Text('_'*100)],
            [sg.Checkbox('Donation Message (100+ bits on twitch)', key='donmsg'), sg.Checkbox('Chat Message',key='chatmsg')],
            [sg.Submit()]  ]

window = sg.Window('Livestream Chat Narrator', layout, resizable=True,)

while True:
    event, values = window.read()
    chat = LiveChat(video_id=values['streamid'][values['streamid'].find('=')+1:])
    if 'youtube.com' in values['streamid'].lower(): #youtube textbox
        if values['donmsg']==True:
            print("youtube stream selected - donation messages selected - program activated")
            window.Refresh()
            while chat.is_alive():
                try:
                    data = chat.get()
                    items = data.items
                    for c in items:
                        if c.amountValue > float(0.0):
                            print(f"{c.datetime} [{c.author.name}] - {c.message} - {c.amountString}")
                            engine = pyttsx3.init()
                            engine.setProperty('rate', 135)
                            engine.say(c.author.name+' donated '+c.amountValue+' and says '+c.message)
                            engine.runAndWait()
                            print('finished playing audio message')
                except KeyboardInterrupt:
                    chat.terminate()
                    break
        if values['chatmsg']==True:
            print("youtube stream selected - all chat messages selected - program activated")
            while chat.is_alive():
                try:
                    data = chat.get()
                    items = data.items
                    for c in items:
                        if c.amountValue > float(0.0):
                            pass
                        else:
                            print(f"{c.datetime} [{c.author.name}] - {c.message}")
                            engine = pyttsx3.init()
                            engine.setProperty('rate', 135)
                            engine.say(c.author.name+' says '+c.message)
                            engine.runAndWait()
                            print('finished playing audio message')
                except KeyboardInterrupt:
                    chat.terminate()
                    break

    if 'twitch.tv' in values['streamid'].lower(): #twitch textbox
        if values['chatmsg']==True:
            print('twitch stream selected - all chat messages selected - program activated')
            with Observer('', 'oauth:') as observer:
                observer.join_channel(values['streamid'][values['streamid'].find('twitch.tv')+10:])
                while True:
                    try:
                        for event in observer.get_events():
                            if event.type == 'TWITCHCHATMESSAGE':
                                print(f"{time.time()} [{event.nickname}] - {event.message}")
                                engine = pyttsx3.init()
                                engine.setProperty('rate', 135)
                                engine.say(event.nickname + ' says ' + event.message)
                                engine.runAndWait()
                    except KeyboardInterrupt:
                        observer.leave_channel(values['streamid'][values['streamid'].find('twitch.tv')+10:])
                        break
        window.refresh()
        if values['donmsg']==True:
            print('twitch stream selected - donation messages selected - program activated')
            with Observer('', 'oauth:') as observer:
                observer.join_channel(values['streamid'][values['streamid'].find('twitch.tv') + 10:])
                while True:
                    try:
                        for event in observer.get_events():
                            if event.type == 'TWITCHCHATMESSAGE':
                                if 'Cheer' in event.message[:5]:
                                    if int(event.message[5:7]) >= 10:
                                        print(f"{time.time()} [{event.nickname}] - {event.message[8:]}")
                                        engine = pyttsx3.init()
                                        engine.setProperty('rate', 135)
                                        engine.say(event.nickname +' donated '+event.message[5:8]+ ' and says ' + event.message[8:])
                                        engine.runAndWait()
                    except KeyboardInterrupt:
                        observer.leave_channel(values['streamid'][values['streamid'].find('twitch.tv') + 10:])
                        break
    if '' in values['streamid'].lower():
        pass
    if event is None:
        window.close()
        break
    else:
        pass