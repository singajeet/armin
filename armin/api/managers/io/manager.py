"""
.. module:: manager
   :platform: Any
   :synopsis: Driver manager for file system
.. moduleauthor:: Ajeet Singh <singajeet@gmail.com>
"""
from typing import Type, Any
from armin.api.share.constants import v_FSC, F
from armin.api.managers.base_manager import BaseDriverManager


class FileSystemManager(BaseDriverManager):
    """DriverManager for accessing file system. This manager will be \
            available under namespace...

    """

    __single_file_system_mgr = None

    def __new__(cls, *args, **kwargs):
        """Singleton instance creator

        """
        if cls != type(cls.__single_file_system_mgr):
            cls.__single_file_system_mgr = object.__new__(cls, *args, **kwargs)
        return cls.__single_file_system_mgr

    def __init__(self):
        """FileSystemManager default constructor

        """
        super(FileSystemManager, self).__init__()

    def load_configuration(self):
        if v_FSC.ACTIVE_DRIVER is not None:
            self._active_driver_name = v_FSC.ACTIVE_DRIVER
        else:
            raise ValueError(
                'Active Driver Name is required. Check your configuration')
        if v_FSC.REPO_DETAILS is not None:
            self._repo_details = v_FSC.REPO_DETAILS
        else:
            raise ValueError('Repo details are required. Check your configuration')
        if v_FSC.ENTRY_POINT_NAMESPACE is not None:
            self._entry_point_namespace = v_FSC.ENTRY_POINT_NAMESPACE
        else:
            raise ValueError(
                'Entry point name space is required. Check configuration')

    def get_invoke_args(self):
        """Returns the arguments required by FileSystemManager

        """
        return (self._active_driver_name, self._repo_details)

    def create_file(self,
                    name: str = None,
                    overwrite: bool = False,
                    base_path: str = None):
        """Creates a new file using the information provided as args

        Args:
            name (str): Full name of an file orfull path to the file
            overwrite (bool): Whether to overwrite if file already exists
            base_path (str): Base or parent path of file incase it is not included in name argument

        Returns:
            result (Status, File): Flag F and File instance

        """
        (status, msg) = self.load_driver(
            'file', (name, self._repo_details, True, base_path, overwrite))
        if status == F.SUCCESS:
            return (status, self._manager.driver)
        else:
            return (status, msg)

    def create_directory(self, name: str = None, overwrite: bool = False):
        """Creates a new dir using the information provided as args

        Args:
            name (str): Full path to the dir
            overwrite (bool): Whether to overwrite if dir already exists

        Returns:
            result (Status, File): Flag F and dir instance

        """
        (status, msg) = self.load_driver(
            'dir', (name, self._repo_details, True, overwrite))
        if status == F.SUCCESS:
            return (status, self._manager.driver)
        else:
            return (status, msg)

    def open_file(self, name: str = None, base_path: str = None):
        """Opens an existing file using the information provided as args

        Args:
            name (str): Full name of an file orfull path to the file
            base_path (str): Base or parent path of file incase it is not included\
        in name argument

        Returns:
            result (Status, File): Flag F and File instance

        """
        (status, msg) = self.load_driver(
            'file', (name, self._repo_details, False, base_path, False))
        if status == F.SUCCESS:
            return (status, self._manager.driver)
        else:
            return (status, msg)

    def open_directory(self, name: str = None):
        """Creates a new dir using the information provided as args

        Args:
            name (str): Full path to the dir

        Returns:
            result (Status, File): Flag F and dir instance

        """
        (status, msg) = self.load_driver(
            'dir', (name, self._repo_details, False, False))
        if status == F.SUCCESS:
            return (status, self._manager.driver)
        else:
            return (status, msg)
