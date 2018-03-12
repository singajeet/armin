"""
.. module:: base_manager
   :platform: Unix, Windows
   :synopsis: Base Driver manager. All driver manager should inherit from this class
.. moduleauthor:: Ajeet Singh <singajeet@gmail.com>

"""
from typing import Any, Type, Tuple, Dict, List
from stevedore import driver
from armin.api.share.constants import F
from armin.api.managers.base_interface import AbstractDriver


class BaseDriverManager(object):
    """An abstract BaseDriverManager to provide default functionality\
    to all derived managers.

    """

    def __init__(self):
        """BaseDriverManager constructor

        """
        self._active_driver_name = None
        self._repo_details = None
        self._entry_point_namespace = None
        self._manager = None
        self._invoke_on_load = True
        self.load_configuration()

    def load_configuration(self) -> Type[F]:
        """Load configuration for current manager. This should be overridden\
        by derived classes

        """
        raise NotImplementedError('This is an abstract method and can'
                                  't be called from instance variable')

    def list_drivers(self) -> Type[List]:
        """Returns the list of all drivers registered under this manager

        """
        if self._manager is not None:
            return self._manager.entry_points_names()
        return None

    def get_invoke_args(self) -> Type[Tuple]:
        """Returns an tuple of args that needs to be passed to driver\
        while invoking it. Thus should be overridden by derived class

        Returns:
            invoke_args (Tuple): Tuple of args that needs to be passed\
        the driver

        """
        raise NotImplementedError('This is an abstract method and can'
                                  't be called from instance variable')

    def load_driver(self,
                    driver_name: str = None,
                    invoke_args: Type[Tuple] = None) -> (Type[F], str):
        """Loads the active driver provided in the configuration or the\
        driver having its name passes as argument to this function

        Args:
           driver_name (str): Name of the driver which needs to be loaded.\
        if no name is provided, active driver will be loaded from configuration\

        import (optional)
           invoke_args (Tuple): A tuple of arguments that needs to be passed\
        to the driver (optional)

        """
        if driver_name is not None:
            self._active_driver_name = driver_name
        _invoke_args = None
        if invoke_args is not None:
            _invoke_args = invoke_args
        else:
            _invoke_args = self.get_invoke_args()
        self._manager = driver.DriverManager(
            namespace=self._entry_point_namespace,
            name=self._active_driver_name,
            invoke_on_load=self._invoke_on_load,
            invoke_args=_invoke_args)
        if self._manager is None:
            return (F.FAILED,
                    'Unable to load driver - %s' % self._active_driver_name)
        return (F.SUCCESS, '')

    def get_driver(self) -> (Type[F], Type[AbstractDriver]):
        """Returns status and instance of active driver

        Returns:
            result (F, AbstractDriver): Returns status flag and instance of active\
        driver

        """
        if self._manager is not None:
            return (F.SUCCESS, self._manager.driver)
        else:
            return (F.FAILED, 'Driver manager is not initialized yet')
