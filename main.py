import PySimpleGUI as sg
from parse_messages import parse_and_show_messages

# All the stuff inside your window. This is the PSG magic code compactor...
layout = [  [sg.Text("Enter your name (used on Facebook):"), sg.InputText()],
            [sg.Text('Enter path to data (messages/inbox dir)')],
            [sg.In(), sg.FolderBrowse()],
            [sg.Text('Filters:')],
            [sg.Text('Show messages between:')],
            [sg.InputText(default_text='2009/10/11'), sg.Text('and'), sg.InputText(default_text='2019/10/11'), 
             sg.Text('(yyyy/mm/dd format) every '), sg.InputText(default_text='7'), sg.Text("days."),],
            [sg.Text('Show people between '), sg.InputText(default_text='0'), 
             sg.Text('th and '), sg.InputText(default_text='10'), sg.Text('th place.')],
            [sg.OK(), sg.Cancel()]]

if __name__ == "__main__":

    # Create the Window
    window = sg.Window('Show Messages Evolution', layout)
    # Event Loop to process "events"
    while True:             
        event, values = window.Read()

        if event in (None, 'Cancel'):
            break
        if event == 'OK':
            try:
                values.pop('Browse')
                parse_and_show_messages(*values.values())
            except Exception as e:
                print(e)

    window.Close()