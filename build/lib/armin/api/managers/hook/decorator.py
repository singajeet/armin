"""
.. module:: decorator
   :platform: Any
   :synopsis: Interface of an hook
.. moduleauthor:: Ajeet Singh <singajeet@gmail.com>
"""
from typing import Type, Any, Callable
from tinydb import Query
from armin.api.share.constants import F, HC, N
from armin.api.managers.hook.interface import AbstractHook, AbstractWrapper
from armin.api.managers.hook.manager import HooksManager

class expose_hook(AbstractHook):
    """Register a method or function as hook point
    Args:
    namespace (str): Register an hook under given namespace. Any other callback\
        registered under this namespace will be called before or after this function\
        executes
    allow_call_type (F): If the value is PRE, only callbacks registered under this\
        namespace for Pre-execution will be called. Other options are POST, BOTH
    """
    def __init__(self, namespace:str, allow_call_type:Type[F]=F.BOTH):
        super(expose_hook, self).__init__(namespace, allow_call_type)
        self.__hook_mgr = HooksManager()
        self.__hook_mgr.register_hook(namespace, allow_call_type)

    def __call__(self, func: Type[Callable]) -> Any:
        """Returns the wrapper, having function passed as arg, wrapped
        """
        (status, msg) = self.__hooks_mgr.load_driver()
        if status == F.SUCCESS:
            (status, result) = self.__hooks_mgr.get_wrapper(self, func)
            if status == F.SUCCESS:
                wrapper = result
                return wrapper
            else:
                raise Exception('Unable to create wrapper for func: %s' % func)
        else:
            raise Exception('Unable to load decorator Wrapper class. Please check your config and make sure driver of type Hooks-Type is installed!')

    def run_pre_callbacks(self, *args, **kwargs):
        """Runs all the callback methods registered under this namespace pre-execution
        """
        for func in self.__hook_mgr.get_pre_callback_list(self._namespace):
                func(*args, **kwargs)

    def run_post_callbacks(self, *args, **kwargs):
        """Runs all the callback methods registered under this namespace post-execution
        """
        for func in self.__hook_mgr.get_post_callback_list(self._namespace):
                func(*args, **kwargs)


class hook_it(AbstractHook):
    """Class to hook a function/callback to a already exposed/registered hook based on a namespace
    """

    def __init__(self, namespace:str, hook_type:Type[F]):
        """Default constructor
        """
        super(hook_it, self).__init__(namespace, hook_type)
        self.__hooks_mgr = HooksManager()

    def __call__(self, func):
        """Registers the func to be called pre or post hook execution
        """
        if self._allow_call_type == F.PRE:
            self.__hooks_mgr.call_before_hook(self._namespace, func)
        elif self._allow_call_type == F.POST:
            self.__hooks_mgr.call_after_hook(self._namespace, func)
        elif self._allow_call_type == F.BOTH:
            self.__hooks_mgr.call_before_hook(self._namespace, func)
            self.__hooks_mgr.call_after_hook(self._namespace, func)
        def wrapper(*args, **kwargs):
            """Just call actual function
            """
            func(*args, **kwargs)
        return wrapper
