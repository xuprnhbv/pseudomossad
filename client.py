from urllib import response
import requests
import json
import base64
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from io import BytesIO


SERVER_ADDRESS = 'http://127.0.0.1'
PICTURE_FIELD = 'lockResponse'
PICTURE_DIMENSIONS = (512, 512)


class BadServerAddressError(Exception): pass


def query_server(token, password, server=SERVER_ADDRESS):
    """
    Sends a request to the server, and returns the parsed response.

    :param token: the token to send to the server
    :param password: the password to send to the server
    :param server: server address and port (address, port)
    :return: a dict of the response. returns empty dict on fail.
    """
    res = requests.post(SERVER_ADDRESS, data={'token': token, 'password': password})
    return json.loads(res.content.decode('utf-8'))

def get_answer(token, password):
    """
    Nicer overhaul of query_server.

    :param token: the token to send to the server
    :param password: the password to send to the server
    :return: tuple of (is_valid, lock_response)
    """
    qu = query_server(token, password)
    return qu['isValid'], qu[PICTURE_FIELD]
        
def popup_image(lock_response):
    popup = Toplevel()
    popup.title('Successfull Authentication!')
    popup.resizable(False, False)
    a = Label(popup, text='Server responded with:').grid()
    img = ImageTk.PhotoImage(Image.open(BytesIO(base64.b64decode(lock_response))).resize(PICTURE_DIMENSIONS))
    imagepanel = Label(popup, image=img)
    imagepanel.grid(row=1)
    popup.mainloop()


def click(window):
    token = window.nametowidget('token').get()
    password = window.nametowidget('password').get()
    main_text = window.nametowidget('main_text')
    text = ''
    fg = ''
    if not token or not password:
        main_text.configure(text='token and password must be filled.', fg='black')
    else:
        try:
            is_valid, response = get_answer(token, password)
            if is_valid:
                main_text.configure(text='Successfull Authentication!', fg='green')
                popup_image(response)
            else:
                main_text.configure(text='Invalid Authentication!', fg='red')
        except (ConnectionError, requests.exceptions.ConnectionError) as e:
            main_text.configure(text=f'Bad connection :(', fg='red')

def setup_ui():
    window = Tk()
    window.title('Supersecret Client')
    window.resizable(False, False)
    window.configure(padx=10, pady=5)
    a = Label(window, text='Enter your supersecret credentials', name='main_text').grid(columnspan=4)
    b = Label(window, text='Token:').grid(row=1)
    token_entry = Entry(window, name='token').grid(row=1, column=1, columnspan=3)
    c = Label(window, text='Password:').grid(row=2)
    pass_entry = Entry(window, name='password').grid(row=2, column=1, columnspan=3)
    submit = Button(window, text='Submit', command=lambda: click(window)).grid(row=3, columnspan=2)
    window.mainloop()

setup_ui()