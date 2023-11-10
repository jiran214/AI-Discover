import functools
import os

from bilibili_api import Credential
from dotenv import load_dotenv


load_dotenv(verbose=True)


@functools.cache
def get_credential():
    attrs = ['sessdata', 'bili_jct', 'buvid3', 'dedeuserid', 'ac_time_value']
    cookie_dict = {attr: os.environ.get(attr, None) for attr in attrs}
    return Credential(**cookie_dict)
