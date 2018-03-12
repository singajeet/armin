"""
.. module:: constants
   :platform: Unix, Windows
   :synopsis: Shared constants and configuration
.. moduleauthor:: Ajeet Singh <singajeet@gmail.com>
"""
from constantly import FlagConstant, Flags
from configparser import ConfigParser, ExtendedInterpolation
import json
import os
import pathlib


class V:
    JSON = 'JSON'
    FILE = 'FILE'
    XML = 'XML'
    HTML = 'HTML'

class N:
    """Docstring for Common.

    """
    NAME = 'NAME'
    DETAILS = 'DETAILS'
    URL = 'URL'
    PASSWORD = 'PASSWORD'
    USERNAME = 'USERNAME'
    PORT = 'PORT'
    TASK = 'action'
    TEMP_FILE = 'TEMP_FILE'
    TEMP_WORKSPACE = 'TEMP_WORKSPACE'
    CHUNK_SIZE = 'CHUNK_SIZE'
    DB_URI = 'DB_URI'
    SOURCE_TABLE = 'SOURCE_TABLE'
    META_TABLE = 'META_TABLE'
    NAMESPACE = 'NAMESPACE'
    ENTRY_POINT = 'ENTRY_POINT'
    CRC = 'CRC'
    DESCRIPTION = 'DESCRIPTION'
    AUTHOR = 'AUTHOR'
    COMPANY = 'COMPANY'
    VERSION = 'VERSION'
    RAISE = 'RAISE'
    RETURN = 'RETURN'
    MARKED_FOR_DELETION = 'MARKED_FOR_DELETION'
    DELETION_TYPE = 'DELETION_TYPE'
    ALLOWED_CALL_TYPE = 'ALLOWED_CALL_TYPE'
    SUBSCRIBERS = 'SUBSCRIBERS'

class F(Flags):
    """

    """
    NONE = FlagConstant()
    SUCCESS = FlagConstant()
    FAILED = FlagConstant()
    PARTIAL = FlagConstant()
    ERROR = FlagConstant()
    WARN = FlagConstant()
    VALID = FlagConstant()
    INVALID = FlagConstant()
    SOFT = FlagConstant()
    HARD = FlagConstant()
    PRE = FlagConstant()
    POST = FlagConstant()
    BOTH = FlagConstant()

class v_GC:
    """Docstring for GenericConstants.

    """
    def __init__(self):
        pass

class ClearValue:
    def __init__(self, val):
        self.val = val

    def clean(self):
        if self.val is not None:
            return self.val.replace('\n', '').replace(' ', '').replace('\'','"')
        else:
            return ''

class v_CONF(object):
    """Base class for value based constants

    """

    __single_v_conf = None

    def __new__(cls, *args, **kwargs):
        """

        """
        if cls != type(cls.__single_v_conf):
            cls.__single_v_conf = object.__new__(cls, *args, **kwargs)
        return cls.__single_v_conf

    def __init__(self):
        """
        Default constructor

        """
        self.CONFIG_FILE = None
        self.__current_module_path = os\
                .path.dirname(os.path.realpath(__file__))
        self.__cwd = pathlib.Path(self.__current_module_path)
        self.__parent_path = self.__cwd.parent
        self.__config_path = self.__parent_path.joinpath('config', 'default.ini')
        self.CONFIG_FILE = os.fspath(self.__config_path)
        self.CONFIG = ConfigParser(interpolation=ExtendedInterpolation())
        self.CONFIG.read(self.CONFIG_FILE)
        self.CONFIG.set('Default', 'app_root_path', str(self.__parent_path))
        with open(self.CONFIG_FILE, 'w') as conffile:
            self.CONFIG.write(conffile)

    def get(self, section, option):
        """Returns an option value from a section

        """
        if self.CONFIG.has_section(section):
            _val = self.CONFIG.get(section, option)
            return _val
        else:
            return None

class HC:
    """Constants for Hooks

    """
    __CONFIG_SECTION_KEY = 'hooks_section'
    __DB_URI_KEY = 'db_uri'
    DB_URI = v_CONF().get(__CONFIG_SECTION_KEY, __DB_URI_KEY)
    __HOOKS_TABLE_KEY = 'hooks_table'
    HOOKS_TABLE = v_CONF().get(__CONFIG_SECTION_KEY, __HOOKS_TABLE_KEY)
    __REPO_DETAILS_KEY = 'repo_details'
    __raw_details = v_CONF().get(__CONFIG_SECTION_KEY, __REPO_DETAILS_KEY)
    REPO_DETAILS = None
    if __raw_details is not None:
        __details = ClearValue(__raw_details).clean()
        REPO_DETAILS = json.loads(__details)
    __ACTIVE_DRIVER_KEY = 'active_driver'
    ACTIVE_DRIVER = v_CONF().get(__CONFIG_SECTION_KEY, __ACTIVE_DRIVER_KEY)
    __ENTRY_POINT_NAMESPACE_KEY = 'entry_point_namespace'
    ENTRY_POINT_NAMESPACE = v_CONF().get(__CONFIG_SECTION_KEY, __ENTRY_POINT_NAMESPACE_KEY)

class v_SC:
    """Constants defined to be used by DefaultSourceDriver

    """
    __CONFIG_SECTION_KEY = 'source_section'
    __DB_URI_KEY = 'db_uri'
    DB_URI = v_CONF().get(__CONFIG_SECTION_KEY, __DB_URI_KEY)
    __SOURCE_TABLE_KEY = 'source_sys_table'
    SOURCE_TABLE = v_CONF().get(__CONFIG_SECTION_KEY, __SOURCE_TABLE_KEY)
    __PACKAGE_EXT_KEY = 'package_ext'
    PACKAGE_EXT = v_CONF().get(__CONFIG_SECTION_KEY, __PACKAGE_EXT_KEY)
    __REPO_DETAILS_KEY = 'repo_details'
    __raw_details = v_CONF().get(__CONFIG_SECTION_KEY, __REPO_DETAILS_KEY)
    REPO_DETAILS = None
    if __raw_details is not None:
        __details = ClearValue(__raw_details).clean()
        REPO_DETAILS = json.loads(__details)
    __ACTIVE_DRIVER_KEY = 'active_driver'
    ACTIVE_DRIVER = v_CONF().get(__CONFIG_SECTION_KEY, __ACTIVE_DRIVER_KEY)
    __ENTRY_POINT_NAMESPACE_KEY = 'entry_point_namespace'
    ENTRY_POINT_NAMESPACE = v_CONF().get(__CONFIG_SECTION_KEY, __ENTRY_POINT_NAMESPACE_KEY)


class v_FSC:
    """Constants defined to be used by FileSystemDriver

    """
    __CONFIG_SECTION_KEY = 'file_system_section'
    __DB_URI_KEY = 'db_uri'
    DB_URI = v_CONF().get(__CONFIG_SECTION_KEY, __DB_URI_KEY)
    __FS_TABLE_KEY = 'file_system_table'
    FS_TABLE = v_CONF().get(__CONFIG_SECTION_KEY, __FS_TABLE_KEY)
    __PACKAGE_EXT_KEY = 'package_ext'
    PACKAGE_EXT = v_CONF().get(__CONFIG_SECTION_KEY, __PACKAGE_EXT_KEY)
    __REPO_DETAILS_KEY = 'repo_details'
    __raw_details = v_CONF().get(__CONFIG_SECTION_KEY, __REPO_DETAILS_KEY)
    REPO_DETAILS = None
    if __raw_details is not None:
        __details = ClearValue(__raw_details).clean()
        REPO_DETAILS = json.loads(__details)
    __ACTIVE_DRIVER_KEY = 'active_driver'
    ACTIVE_DRIVER = v_CONF().get(__CONFIG_SECTION_KEY, __ACTIVE_DRIVER_KEY)
    __ENTRY_POINT_NAMESPACE_KEY = 'entry_point_namespace'
    ENTRY_POINT_NAMESPACE = v_CONF().get(__CONFIG_SECTION_KEY, __ENTRY_POINT_NAMESPACE_KEY)


class v_PC:
    """Constants defined to be used by Package related files

    """
    __CONFIG_SECTION_KEY = 'package_section'
    __ALLOWED_SCRIPT_EXT_KEY = 'allowed_setup_script_ext'
    ALLOWED_SCRIPT_EXT = v_CONF().get(__CONFIG_SECTION_KEY, __ALLOWED_SCRIPT_EXT_KEY)
    ARG_LIST_FOR_SCRIPT_KEY = 'setup_args'
    SETUP_FILE_KEY = 'setup_file'
    SETUP_SECTION_KEY = 'setup_section'
