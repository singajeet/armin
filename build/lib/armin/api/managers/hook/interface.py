"""
.. module:: interface
   :platform: Any
   :synopsis: Interface of an hook
.. moduleauthor:: Ajeet Singh <singajeet@gmail.com>
"""
from typing import Type, Any, Callable
from armin.api.share.constants import F


class AbstractHook(object):
    """Abstract class for an hook
    """
    def __init__(self, namespace:str, allow_call_type:Type[F]=F.BOTH):
        """
        """
        self._namespace = namespace
        self._allow_call_type = allow_call_type

    def __call__(self, func: Type[Callable]) -> Any:
        """
        """
        pass

    def run_pre_callbacks(self, *args, **kwargs) -> (Type[F], str):
        """
        """
        pass

    def run_post_callbacks(self, *args, **kwargs) -> (Type[F], str):
        """
        """
        pass


class AbstractWrapper(object):
    """An abstract wrapper class for decorators
    """
    def __init__(self):
        """default constructor
        """
        pass

    def __copy__(self):
        """Creates shallow copy of an instance
        """
        pass

    def wrap(self, decorator, func):
        """wraps an function to give new behaviour
        """
        def wrapped_func(*args, **kwargs):
            """
            """
            decorator.run_pre_callbacks()
            func(*args, **kwargs)
            decorator.run_post_callbacks()
        return wrapped_func
