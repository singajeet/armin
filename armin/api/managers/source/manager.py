"""
.. module:: manager
   :platform: Unix, Windows
   :synopsis: Driver manager for source system related plugins
"""
from typing import Any, Type, Dict, Tuple
from armin.api.managers.source import interface
from stevedore import driver
from armin.api.share.constants import v_SC, F
from armin.api.managers.base_manager import BaseDriverManager


class SourceDriverManager(BaseDriverManager):
    """DriverManager for managing source system related drivers.
    """

    __single_source_driver_mgr = None

    def __new__(cls, *args, **kwargs):
        """Single object creator
        """
        if cls != type(cls.__single_source_driver_mgr):
            cls.__single_source_driver_mgr = object.__new__(cls, *args, **kwargs)
        return cls.__single_source_driver_mgr

    def __init__(self):
        """SourceDriverManager constructor to initialize the singleton instance of this class.

        Example:

            >>> from armin.api.managers.source.manager import SourceDriverManager
            >>> mgr = SourceDriverManager()
            >>> mgr is not None
            True

        Note:
            As of now this class is not thread safe and is a singleton which will be shared among many objects.

        """
        super(SourceDriverManager, self).__init__()

    def load_configuration(self) -> Type[F]:
        if v_SC.ACTIVE_DRIVER is not None:
            self._active_driver_name = v_SC.ACTIVE_DRIVER
        else:
            raise ValueError('Active Driver Name is required. Check your configuration')
        if v_SC.REPO_DETAILS is not None:
            self._repo_details = v_SC.REPO_DETAILS
        else:
            raise ValueError('Repo Details are required. Check your configuration')
        if v_SC.ENTRY_POINT_NAMESPACE is not None:
            self._entry_point_namespace = v_SC.ENTRY_POINT_NAMESPACE
        else:
            raise ValueError('Entry point namespace is required. Check your configuration')

    def get_invoke_args(self) -> Type[Tuple]:
        return (self._active_driver_name, self._repo_details,)

    def get_source_system_driver(self) \
            -> (Type[F], Type[interface.AbstractSourceDriver]):
        """Returns instance of the plugin driver loaded
        """
        return self.get_driver()
