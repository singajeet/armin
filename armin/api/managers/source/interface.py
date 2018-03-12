"""
.. module:: interface
   :platform: Windows, Unix
   :synopsis: An abstract driver class for accessing source system

.. moduleauthor:: Ajeet Singh <singajeet@gmail.com>
"""
import aiohttp
from asyncio import Future
from typing import Any, Dict, Type
import os
import tempfile
from async_generator import asynccontextmanager
from armin.api.share.constants import F, V, N
from armin.api.managers.base_interface import AbstractDriver


class AbstractSourceDriver(AbstractDriver):
    """An base class for an source system

    """

    def __init__(self, name: str, repo_details: Type[Dict] = None):
        """Constructor for abstract source driver class
        Args:
            name (str): Name of the source system
            repo_details (Dict): A dict containing config to connect to meta\
                    repository

        """
        super(AbstractSourceDriver, self).__init__(name, repo_details)
        self._name = name
        self._details = {
            N.URL: None,
            N.PORT: 80,
            N.USERNAME: None,
            N.PASSWORD: None,
            N.CHUNK_SIZE: 1024,
            N.TASK: 'index',
            N.TEMP_FILE: None
        }
        self._input_dict = None
        self._meta_repo_details = repo_details
        self.connect_to_meta()
        self._prepare_temp_file()

    def set_meta(self, url: str = None, port :int = None, user_name: str = None,\
                 password: str = None, chunk_size: int = None, task: str = None):
        """Set url of source system

        Args:
            url (str): Url pointing to source system

        """
        if url is not None:
            self._details[N.URL] = url
        if port is not None:
            self._details[N.PORT] = port
        if user_name is not None:
            self._details[N.USERNAME] = user_name
        if password is not None:
            self._details[N.PASSWORD] = password
        if chunk_size is not None:
            self._details[N.CHUNK_SIZE] = chunk_size
        if task is not None:
            self._details[N.TASK] = task
        #creates a valid temp file if not exists
        self._prepare_temp_file()
        #saves the metadata of this driver to repo
        self.save()
        if url is None and self._details[N.URL] is None:
            raise ValueError('Invalid Url provided')

    def _prepare_temp_file(self):
        """Prepares the temp file for use in operations

        """
        if not self._details.__contains__(N.TEMP_FILE) or \
           self._details[N.TEMP_FILE] is None:
            _temp_file = tempfile.NamedTemporaryFile(delete=False)
            self._details[N.TEMP_FILE] = _temp_file.name
            _temp_file.close()
            return
        if not os.path.exists(self._details[N.TEMP_FILE]):
            _temp_file = tempfile.NamedTemporaryFile(delete=False)
            self._details[N.TEMP_FILE] = _temp_file.name
            _temp_file.close()

    def put_input(self, input_details: Type[Dict]=None) -> (Type[F], str):
        """Prepares the input for source system

        Args:
            input_details (Dict): formats the input for source system

        Returns:
            status (F, str): Flag F and message in case of failure

        """
        if input_details is None:
            return (F.WARN, '**WARNING** => Empty input! A possible incorrect\
                    params')
        self._dict_input = input_details
        return (F.SUCCESS, '')

    def add_input(self, key, value):
        """Add a key-value pair to the input dict to source system

        Args:
            key (str): Unique identifier for an input
            value (str): Value of the input

        """
        if self._dict_input is None:
            self._dict_input = {}
        self._dict_input[key] = value
        return (F.SUCCESS, self._dict_input)

    def get_input(self, key):
        """Returns value of input if available

        Args:
            key (str): Identifier for an item in input dict

        """
        if key is not None and self._dict_input is not None:
            return self._dict_input[key]
        return None

    def has_input(self, key):
        """Check if input exists in input dict

        """
        if key is not None and self._dict_input is not None:
            if self._dict_input.__contains__(key):
                return True
        return False

    def get_input_dict(self):
        """Returns all inputs available as dict

        """
        return self._dict_input

    def get_meta(self, key):
        """Returns value of meta item from meta dict based on key passed

        Args:
            key (str): Key to find item in meta dict

        """
        if key is not None:
            return self._details[key]
        return None

    def has_meta(self, key):
        """Returns True or False after checking key in meta dict

        """
        if self._details.__contains__(key):
            return True
        return False

    def connect_to_meta(self) -> (Type[F], str):
        """When overridden in derived class provides function to connect \
                with meta repo. Meta repo stores information about the \
                system like connection details, etc

        Returns:
            status (F, str): Flag F  based on connection \
                    status, i.e., connected or not connected and message \
                    string in case of failure

        """
        raise NotImplementedError('This is an abstract method and can''t be \
                                  called from instance variable')

    def save(self) -> (Type[F], str):
        """Save the details of source in meta repo

        Returns:
            status (F): Flag F

        """
        raise NotImplementedError('This is an abstract method and can''t be\
                                  called from instance variable')

    def update(self, details: Type[Dict] = None) -> (Type[F], str):
        """Update details of source in meta repo

        Args:
            details (dict): Details of source system in dict form

        Returns:
            status (F, str): Flag F and message

        """
        raise NotImplementedError('This is an abstract method and can''t be\
                                  called from instance variable')

    def prepare_to_connect(self, loop) -> (Type[F], str):
        """Prepares the connection to an source system using details saved\
                in meta and executes tasks as coroutines on the loop passed in\
                as parameter to this function

        Args:
            loop (EventLoop): :class:`asyncio`.loop which will be used to run\
                    coroutines

        Returns:
            status (bool): True or False

        """
        raise NotImplementedError('This is an abstract method and can''t be\
                                  called from instance variable')

    async def perform_task(self, task: str = None,\
                           expected_result_type: Type[V] = V.JSON)\
            -> Type[Future]:
        """Signals source system to perform an task. Task name should \
                be passed to this function as parameter

        Args:
            task (str): Name of task available on source system
            expected_result_type (V): Constant options of type V

        Returns:
            future (Future): An instance of async Future callback

        """
        raise NotImplementedError('This is an abstract method and can''t be\
                                  called from instance variable')

    async def get_output(self) -> (Type[F], Any):
        """Returns result of an operation performed in source system

        """
        raise NotImplementedError('This is an abstract method and can''t be\
                                  called from instance variable')
