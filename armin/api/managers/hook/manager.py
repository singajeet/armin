"""
.. module:: manager
   :platform: Any
   :synopsis: Manage various hooks in the system
.. moduleauthor:: Ajeet Singh <singajeet@gmail.com>
"""
from typing import Type, Callable
from stevedore import driver
from armin.api.managers.base_manager import BaseDriverManager
from armin.api.share.constants import HC, F

class HooksManager(BaseDriverManager):
    """A manager class for hooks
    """

    __single_hooks_manager = None

    def __new__(cls, *args, **kwargs):
        """Singleton pattern implementation
        """
        if cls != type(cls.__single_hooks_manager):
            cls.__single_hooks_manager = object.__new__(cls, *args, **kwargs)
        return cls.__single_hooks_manager

    def __init__(self):
        """Default constructor for HooksManager
        """
        super(HooksManager, self).__init__()
        self._pre_callbacks_repo = {}
        self._post_callbacks_repo = {}

    @property
    def pre_callbacks_repo(self):
        """A callback repo of funcs that needs to be called pre-hook execution
        """
        return self._pre_callbacks_repo

    @property
    def post_callbacks_repo(self):
        """A callback repo of funcs that needs to be called post-hook execution
        """
        return self._post_callbacks_repo

    def get_pre_callback_list(self, namespace_filter=None):
        """Returns a list of pre-execution callbacks. If filter arg is provided, only callbacks registered under a namespace will be returned
        """
        if namespace_filter is not None:
            if self._pre_callbacks_repo.__contains__(namespace_filter):
                return self._pre_callbacks_repo[namespace_filter]
            else:
                return None
        else:
            _all_cb_list = []
            for name, cb_list in self._pre_callbacks_repo.items():
                _all_cb_list.extend(cb_list)
            return _all_cb_list

    def get_post_callback_list(self, namespace_filter=None):
        """Returns a list of post-execution callbacks. If filter arg is provided, only callbacks registered under a namespace will be returned
        """
        if namespace_filter is not None:
            if self._post_callbacks_repo.__contains__(namespace_filter):
                return self._post_callbacks_repo[namespace_filter]
            else:
                return None
        else:
            _all_cb_list = []
            for name, cb_list in self._post_callbacks_repo.items():
                _all_cb_list.extend(cb_list)
            return _all_cb_list

    def load_configuration(self) -> Type[F]:
       """Loads the configuration for connecting to meta repo, etc
       """
       if HC.ACTIVE_DRIVER is not None:
           self._active_driver_name = HC.ACTIVE_DRIVER
       else:
           raise Exception('Active Driver property is required. Please check your config')
       if HC.ENTRY_POINT_NAMESPACE is not None:
           self._entry_point_namespace = HC.ENTRY_POINT_NAMESPACE
       else:
           raise Exception('Entry point namespace is required. Check your config')

    def get_invoke_args(self):
        """No args to pass
        """
        return None

    def get_wrapper(self, decorator, func):
        """Returns the wrapper created on the actual function
        """
        (status, result) = self.get_driver()
        wrapper = result.copy()
        if status == F.SUCCESS:
            return (F.SUCCESS, wrapper.wrap(decorator, func))
        return (F.FAILED, result)

    def register_hook(self, namespace:str, call_type:Type[F]=F.BOTH):
        """Registers an hook under given namespace and call type
        """
        if namespace is None:
            raise ValueError('Namespace is an required field')
        if call_type == F.BOTH:
            __register_under_pre(namespace)
            __register_under_post(namespace)
        elif call_type == F.PRE:
            __register_under_pre(namespace)
        elif call_type == F.POST:
            __register_under_post(namespace)
        else:
            raise ValueError('Invalid call type provided')

    def __register_under_pre(self, namespace:str):
        """Registers a new namespace
        """
        if self._pre_callbacks_repo.__contains__(namespace):
            raise ValueError('Specified namespace is already in use. Please choose a different one')
        self._pre_callbacks_repo[namespace]=[]

    def __regiser_under_post(self, namespace:str):
        """Registers a new namespace
        """
        if self._post_callbacks_repo.__contains__(namespace):
            raise ValueError('Specified namespace is already in use. Please choose a different one')
        self._post_callbacks_repo[namespace]=[]

    def call_before_hook(self, namespace:str, func:Type[Callable]):
        """Register an func/callback to be called before calling hook
        """
        if namespace is not None and func is not None:
            if self._pre_callbacks_repo.__contains__(namespace):
                func_list = self._pre_callbacks_repo[namespace]
                func_list.append(func)
            else:
                raise ValueError('Namespace is not registered yet: %s' % namespace)
        else:
            raise ValueError('Either namespace or func passed as arg is not valid')

    def call_after_hook(self, namespace:str, func:Type[Callable]):
        """Register an func/callback to be called after calling hook
        """
        if namespace is not None and func is not None:
            if self._post_callbacks_repo.__contains__(namespace):
                func_list = self._post_callbacks_repo[namespace]
                func_list.append(func)
            else:
                raise ValueError('Namespace is not registered yet: %s' % namespace)
        else:
            raise ValueError('Either namespace or func passed as arg is not valid')
