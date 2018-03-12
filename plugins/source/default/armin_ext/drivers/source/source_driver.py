"""
.. module:: source_driver
   :platform: Unix, Windows
   :synopsis: A default implementation of source system driver
"""
import asyncio
import aiohttp
import pathlib
from typing import Type, Dict, Any
from tinydb import TinyDB, Query, where
from armin.api.share import sessions
from armin.api.managers.source.interface import AbstractSourceDriver
from armin.api.managers.io.manager import FileSystemManager
from armin.api.share.constants import V, N, F, v_SC
from armin.api.share import utils



class DefaultSourceDriver(AbstractSourceDriver):
    """Default implementation of source system driver using HTTP protocol

    """

    def __init__(self, name: str, repo_details: Type[Dict] = None):
        """Default constructor

        Args:
            name (str): Name of the source system driver

        """
        super(DefaultSourceDriver, self).__init__(name, repo_details)
        self.__source_sys_meta_table = None
        self.__is_new = False
        self.__session = None
        self.__dict_input = {}
        self.__expected_result_type = V.JSON
        self.__response = None

    def connect_to_meta(self) -> (Type[F], str):
        """Connect to metadata database using the details provided as\
                parameters in the constructor

        Returns:
            status (Tuple): Returns flag Success or Failed and details\
                    in case of failure

        """
        (status, _record) = utils.connect_to_meta(self.meta_repo_details, self.name)
        if status == F.SUCCESS and _record is not None:
            self._details = _record[N.DETAILS]
            self.__source_sys_meta_table = utils.get_meta_table(self.meta_repo_details)
        else:
            return (status, _record)
        if self._details is None or len(self._details) <= 0:
            self.__is_new = True
        return (F.SUCCESS, '')

    def save(self) -> (Type[F], str):
        """Saves details about source system in meta repo

        """
        if self._details is not None:
            if self.__source_sys_meta_table is not None:
                (__valid, reason) = self.__validate()
                if not __valid:
                    return (__valid, reason)
                if self.__is_new is False:
                    self.__source_sys_meta_table\
                            .update({N.DETAILS: self._details}, \
                                    Query()[N.NAME] == self._name)
                else:
                    __exists = self.__source_sys_meta_table\
                            .count(where(N.NAME) == self._name)
                    if __exists:
                        return (F.FAILED,\
                                'Record with similar name (%s) already exists'\
                                % self._name)
                    self.__source_sys_meta_table\
                            .insert({N.NAME: self._name, N.DETAILS: self._details})
                    self.__is_new = False
                return (F.SUCCESS, '')
            else:
                return (F.FAILED, 'Source system meta table not found in repo')
        else:
            return (F.FAILED, 'Can not save empty details')

    def update(self, details: Type[Dict] = None) -> (Type[F], str):
        """Saves the details of source system in meta repo. \
                if details are passed as argument same will be used to override\
                existing details in repo

        Args:
            details (dict): An dict of source system details

        Returns:
            status (F, msg): Success or Failed and message in case of failure

        """
        if details is not None:
            self._details = details
        return self.save()

    def __validate(self) -> (Type[F], str):
        """Validates the details dict to make sure all required attributes are\
                available

        Returns:
            status (F, str): Success or Failed and message in case of invalid

        """
        if self._details is None:
            return (F.FAILED, 'Details dict can''t be null')
        if len(self._details) < 1:
            return (F.FAILED, 'Number of attributes in details dict do not match\
                    with number of attributes required - %d' % 1)
        if not self._details.__contains__(N.URL):
            return (F.FAILED, '%s missing from details dict')
        if not self._details.__contains__(N.PASSWORD) \
           or not self._details.__contains__(N.USERNAME) \
           or not self._details.__contains__(N.PORT):
            return (F.WARN, '**WARNING** => Possible missing important \
                    attributes, please check')
        return (F.SUCCESS, '')

    def prepare_to_connect(self, loop: Type[asyncio.unix_events.SelectorEventLoop])\
            -> (Type[F], str):
        """Connects to the source system using details available in dict

        Args:
            loop (asyncio.loop): Current event loop running on current or some\
                    other thread

        Returns:
            status (F, str): Success or Failed and message in case of failure

        """
        self.__session = sessions.Web(loop).SESSION

    async def perform_task(self, task: str = None,\
                           expected_result_type: Type[V] = V.JSON)\
            -> (Type[asyncio.Future]):
        """Calls the task on source system

        Args:
            task (str): Name of the task to perform \
                    (optional, default = action from configuration)
            expected_result_type (V): Returns the type of result \
                    (V.JSON, V.FILE...) (optional, default is V.JSON)

        Returns:
            response (Response): An instance of Response

        """
        if self.__session is None:
            raise RuntimeError('Session not initialized yet! Please call \
                           :meth:`prepare_to_connect`() before calling \
                           this method')
        self.__expected_result_type = expected_result_type
        if self.has_meta(N.TASK):
            self.add_input(N.TASK, self.get_meta(N.TASK))
        if task is not None:
            self.add_input(N.TASK, task)
        async with self.__session\
                .get(self.get_meta(N.URL),
                     params = self.get_input_dict()) as response:
            self.__response = response
            return self.__response

    async def get_output(self) -> (Type[F], Any):
        """Returns the output of the task performed on source

        Returns:
            (F, Any): returns the result flag F along with result

        """
        if self.__response is None:
            return (F.FAILED, 'No task is executted yet')
        if self.__expected_result_type == V.JSON:
            result = await self.__response.json()
            self.__response.close()
            if result is not None:
                return (F.SUCCESS, result)
            else:
                return (F.WARN, '**WARNING** => result is empty, possible\
                        incorrect results')
        elif self.__expected_result_type == V.FILE:
            response_stream = self.__response
            temp_path = ''
            if self._details.__contains__(N.TEMP_FILE):
                temp_path = self._details[N.TEMP_FILE]
            if temp_path is None:
                temp_path = '~/.source'
            if temp_path is not None:
                with open(temp_path, 'wb') as fd:
                    while True:
                        chunk = await response_stream.content\
                                .read(self._details[N.CHUNK_SIZE])
                        if not chunk:
                            break
                        fd.write(chunk)
                _fs_mgr = FileSystemManager()
                (status, _file_driver) = _fs_mgr.open_file(name=temp_path)
                response_stream.close()
                if status == F.SUCCESS:
                    return (F.SUCCESS, _file_driver)
            return (F.WARN, 'Server call was successful but unable to save\
                    content locally')
        return (F.FAILED, 'Unknown result type found')
