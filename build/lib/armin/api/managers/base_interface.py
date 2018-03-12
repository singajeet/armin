"""
.. module:: base_interface
   :platform: Windows, Unix
   :synopsis: An abstract driver class
.. moduleauthor:: Ajeet Singh <singajeet@gmail.com>
"""
import aiohttp
from asyncio import Future
from typing import Any, Dict, Type
from armin.api.share.constants import F, V


class AbstractDriver(object):
    """An base class for an source system
    """

    def __init__(self, name: str, repo_details: Type[Dict] = None):
        """Constructor for abstract source driver class

        Args:
           name (str): Name of the source system
           repo_details (Dict): A dict containing config to connect to meta repository

        """
        self._id = None
        self._name = name
        self._details = {}
        self._meta_repo_details = repo_details

    def set_meta(self, details: Type[Dict] = None):
        """Adds meta details to be consumed by driver

        Args:
           details (dict): A meta details dict having key-value pairs to be used by driver

        """
        if details is not None:
            self._details = details
        else:
            raise ValueError('Can' 't add empty meta details')

    def connect_to_meta(self) -> (Type[F], str):
        """When overridden in derived class provides function to connect with meta repo.
            Meta repo stores information about the system like connection details, etc

        Returns:
           status (F, str): Flag F  based on connection status, i.e., connected or
           not connected and message string in case of failure

        """
        raise NotImplementedError(
            'This is an abstract method and cant be called from instance variable'
        )

    def save(self) -> (Type[F], str):
        """Save the details of source in meta repo

        Returns:
           status (F): Flag F

        """
        raise NotImplementedError('This is an abstract method and can'
                                  't be called from instance variable')

    def update(self, details: Type[Dict] = None) -> (Type[F], str):
        """Update details of source in meta repo

        Args:
           details (dict): Details of source system in dict form

        Returns:
           status (F, str): Flag F and message

        """
        raise NotImplementedError('This is an abstract method and can'
                                  't be called from instance variable')
