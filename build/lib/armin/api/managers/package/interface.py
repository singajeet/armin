"""
.. module:: interface
   :platform: Unix, Windows
   :synopsis: Interface to a package in package management system

.. moduleauthor:: Ajeet Singh <singajeet@gmail.com>
"""

#imports ---------------------------------
from typing import Dict, Type, List, Any
from configparser import ConfigParser
from armin.api.share.constants import F, N
from armin.api.share.validations import Validator



class AbstractPackage(object):
    """:class:`AbstractPackage` class contains information about a package in the \
            Package Managment System. A package consist of one or more components \
            grouped logically together. If there is an dependency between components \
            and other packages, same will be defined in this class

    """

    def __init__(self, name: str, repo_details: Type[Dict]):
        """Default constructor for an package

        """
        self._name = name
        self._repo_details = repo_details
        #-- read-only or validation-enabled props--
        self._id = None
        self._source_id = None
        self._package_file_id = None
        self._fs_id = None
        self._category = None
        self._is_enabled = True
        self._is_installed = False
        self._components = {}
        self._build_type_id = None
        self._package_dependencies = {}
        #-- public props, no validation req --
        self._meta = {
            N.TEMP_WORKSPACE: None,
            N.NAMESPACE: None,
            N.ENTRY_POINT: None,
            N.CRC: None,
            N.DESCRIPTION: None,
            N.AUTHOR: None,
            N.URL: None,
            N.COMPANY: None,
            N.VERSION: None,
        }
        self.connect_to_meta()
        self._prepare_temp_workspace()

    @property
    def category(self):
        """Category of an package

        """
        return self._category

    @category.setter
    def category(self, value):
        self._category = value

    @property
    def is_enabled(self):
        """Flag which denotes whether package is in use or not

        """
        return self._is_enabled

    @is_enabled.setter
    def is_enabled(self, value):
        self._is_enabled = value

    @property
    def is_installed(self):
        """As name suggest, this flag tells whether package is installed or not

        """
        return self._is_installed

    @is_installed.setter
    def is_installed(self, value):
        self._is_installed = value

    def set_source_id(self, id: str) -> Type[F]:
        """Sets the identifier of source system from where this package will be sourced

        Args:
            id (str): Unique id of the source system (i.e., source-driver)

        """
        if id is not None:
            self._source_id = id
            return F.SUCCESS
        return F.FAILED

    def get_source_id(self) -> str:
        """Returns the id of source system

        """
        return self._source_id

    def set_package_file_id(self, id) -> Type[F]:
        """Sets the id of physical package file

        """
        if id is not None:
            self._package_file_id = id
            return F.SUCCESS
        return F.FAILED

    def get_package_file_id(self) -> str:
        """Returns id of physical file

        """
        return self._package_file_id

    def set_fs_id(self, id) -> Type[F]:
        """Sets the id of fs path id where pkg is installed

        """
        if id is not None:
            self._fs_id = id
            return F.SUCCESS
        return F.FAILED

    def get_fs_id(self) -> str:
        """Returns id of fs path where package is installed

        """
        return self._fs_id

    def get_setup_config(self) -> Type[ConfigParser]:
        """Returns config instance for this package

        """
        pass

    def get_setup_script_args(self) -> Type[List]:
        """Returns a list of args that needs to be passed to setup script

        """
        pass

    def get_setup_script_path(self) -> str:
        """Returns path to the setup script for this package

        """
        pass

    def save(self) -> (Type[F], str):
        """Saves the data available in local meta to the meta repository

        """
        pass

    def remove(self, hard: bool=False) -> (Type[F], str):
        """Removes the package from the meta repo. If "hard" arg is true,\
        it will removes the meta from repo as well as the files from the file system

        """
        pass

    def set_meta(self, namespace:str=None, entry_point:Type[Dict]=None, description:str=None, crc:str=None, author:str=None, company:str=None, url:str=None) -> Type[F]:
        """Sets whole meta dict or key-value pair of meta. All params can't be set blank

        """
        pass

    def get_meta(self, key) -> Type[Any]:
        """Returns value of meta for which key is passed

        """
        pass

    def set_custom_meta(self, key, value):
        """Sets an custom meta for the package

        Args:
            key (str): key for an custom meta item
            value (str): value of meta

        """
        if Validator().not_none(self._meta).not_empty(key).not_none(value).validate():
            self._meta[key] = value

    def get_custom_meta(self, key):
        """Returns custom meta value if available

        """
        if Validator().not_empty(key).validate() and self._meta.__contains__(key):
            return self._meta[key]
        return None

    def set_dependency(self, package):
        """Set current packages dependency on the package passed as args

        """
        pass

    def get_dependencies(self):
        """Returns an dict of dependencies for current package

        """
        pass

    def connect_to_meta(self) -> (Type[F], str):
        """Connect to meta repo

        """
        pass

    def _prepare_temp_workspace(self):
        """Prepares an temp workspace dir to be used by this package

        """
        pass

    def get_installer(self):
        """Returns installer of current package

        """
        pass

    def install_meta(self) -> (Type[F], str):
        """Install package meta to the system. Will be called by installer

        """
        pass

    def list_components(self) -> Type[List]:
        """Returns a list containing name of all components available in this package

        Returns:
            comp_name_list ([str]): List of component names available in this package

        """
        return [name for name, obj in self._components.items()]

    def get_components(self) -> Type[Dict]:
        """Returns instances of all components which are part of this package

        Returns:
            components (Dict): Returns dict of components

        """
        if self._components is not None:
            return self._components
        return None

    def get_component(self, name) -> Type[Any]:
        """Returns an instance of component if available in dict

        Args:
            name (str): Name of the component which needs to be returned

        Returns:
            Instance of component if found else None

        """
        if self._components is not None:
            if self._components.__contains__(name):
                return self._components[name]
        return None

    def get_component_by_id(self, comp_id) -> Type[Any]:
        """Same as :meth:`get_component` but returns the component based on id

        Args:
            comp_id (uuid): The unique id assigned to an component

        Returns:
            An instance of component or None

        """
        if self._components is not None and comp_id is not None:
            for name, comp_obj in self._components.items():
                if comp_obj.id == comp_id:
                    return comp_obj
            return None

    def get_components_name_id_map(self) -> Type[Dict]:
        """Returns an dict of name-to-id mapping of all components in this package

        """
        _map = {}
        for name, comp_obj in self._components.items():
            _map[name] = comp_obj.id
        return _map

