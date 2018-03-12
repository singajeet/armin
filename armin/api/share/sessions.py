"""
.. module:: package
   :platform: Unix, Windows
   :synopsis: Package management functionality

.. moduleauthor:: Ajeet Singh <singajeet@gmail.com>
"""
import aiohttp
import asyncio
from typing import Type


class Web(object):
    """Provides session for accessing web resources
    """

    __single_web_session = None
    SESSION = None

    def __new__(cls, loop):
        """Class instance creator
        """
        if cls != type(cls.__single_web_session):
            cls.__single_web_session = object.__new__(cls)
            cls.SESSION = aiohttp.ClientSession(loop=loop)
            #cls.__single_web_session.__init__(loop)
        return cls.__single_web_session

    #def __init__(self, loop: asyncio.unix_events.SelectorEventLoop = None):
        """Web session instance creator
        """
        #self._SESSION = aiohttp.ClientSession(loop=loop)

    #@property
    #def SESSION(self):
        """A single instance web session property
        """
       # return self._SESSION
