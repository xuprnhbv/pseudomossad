from urllib import response
import requests
import json
import base64
import re
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from io import BytesIO


HTTP_PRE = 'http://{}'
IP_REGEX = r"^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)(\.(?!$)|$)){4}$"
PICTURE_FIELD = 'lockResponse'
PICTURE_DIMENSIONS = (512, 512)


def query_server(token, password, server):
    """
    Sends a request to the server, and returns the parsed response.

    :param token: the token to send to the server
    :param password: the password to send to the server
    :param server: server address and port (address, port)
    :return: a dict of the response. returns empty dict on fail.
    """
    res = requests.post(HTTP_PRE.format(server), data={
                        'token': token, 'password': password})
    return json.loads(res.content.decode('utf-8'))


def get_answer(token, password, server):
    """
    Nicer wrap of query_server.

    :param token: the token to send to the server
    :param password: the password to send to the server
    :return: tuple of (is_valid, lock_response)
    """
    qu = query_server(token, password, server)
    return qu['isValid'], qu[PICTURE_FIELD]


def popup_image(lock_response):
    """
    Creates popup for success.

    :param lock_response: a base64 encoded picture, to be displayed.
    """
    popup = Toplevel()
    popup.title('Successfull Authentication!')
    popup.resizable(False, False)
    a = Label(popup, text='Server responded with:').grid()
    img = ImageTk.PhotoImage(Image.open(
        BytesIO(base64.b64decode(lock_response))).resize(PICTURE_DIMENSIONS))
    imagepanel = Label(popup, image=img)
    imagepanel.grid(row=1)
    popup.mainloop()


def click(window):
    """
    Collects data from entries and queries the server. Also handles empty field values etc.

    :param window: the root window
    """
    token = window.nametowidget('token').get()
    password = window.nametowidget('password').get()
    address = window.nametowidget('server').get()
    main_text = window.nametowidget('main_text')
    if not re.match(IP_REGEX, address):
        main_text.configure(text="invalid ipv4 address", fg='black')
    elif not token or not password:
        main_text.configure(
            text='token and password must be filled.', fg='black')
    else:
        try:
            is_valid, response = get_answer(token, password, address)
            if is_valid:
                main_text.configure(
                    text='Successfull Authentication!', fg='green')
                popup_image(response)
            else:
                main_text.configure(text='Invalid Authentication!', fg='red')
        except (ConnectionError, requests.exceptions.ConnectionError):
            main_text.configure(text=f'Bad connection :(', fg='red')
        except json.decoder.JSONDecodeError:
            main_text.configure(text="Invalid response :(", fg='red')


def setup_ui():
    """
    Initial function. Set ups the root window and begins the UI.
    """
    window = Tk()
    window.title('SEC')
    window.resizable(False, False)
    window.configure(padx=10, pady=5)
    Label(window, text='Enter your supersecret credentials',
              name='main_text').grid(columnspan=4)
    Label(window, text='Server:').grid(row=1)
    Entry(window, name='server').grid(row=1, column=1, columnspan=3)
    Label(window, text='Token:').grid(row=2)
    Entry(window, name='token').grid(
        row=2, column=1, columnspan=3)
    Label(window, text='Password:').grid(row=3)
    Entry(window, name='password').grid(
        row=3, column=1, columnspan=3)
    Button(window, text='Submit', command=lambda: click(
        window)).grid(row=4, columnspan=2)
    window.mainloop()


if __name__ == '__main__':
    setup_ui()
