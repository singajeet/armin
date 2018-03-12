"""
.. module:: interface
   :platform: Any
   :synopsis: Interface definitions for io related managers

.. moduleauthor:: Ajeet Singh <singajeet@gmail.com>
"""
import os
import pathlib
from typing import Type, List, Dict, Any
from goldfinch import validFileName
from armin.api.managers.base_interface import AbstractDriver
from armin.api.share.constants import F


class AbstractIODriver(AbstractDriver):
    """Base class of an object represents in filesystem

    """

    def __init__(self, name: str = None, repo_details: Type[Dict] = None):
        """Default constructor for an io object

        Args:
            name (str): Name of an io object
            repo_details (dict): Repository configuration details

        """
        super(AbstractIODriver, self).__init__(name, repo_details)
        self._name = name
        self._os_name = None
        self._machine_name_on_network = None
        self._os_release = None
        self._os_version = None
        self._machine_name = None
        (self._os_name, self._machine_name_on_network, self._os_release,
         self._os_version, self._machine_name) = os.uname()

    @property
    def name(self) -> str:
        """Name property of an IO object
        """
        return self._name

    @name.setter
    def name(self, value):
        self._name = validFileName(value, initCap=False).decode('utf8')


class AbstractDirDriver(AbstractIODriver):
    """An Abstract class representing a directory
    """

    def __init__(self,
                 name: str,
                 repo_details: Type[Dict] = None,
                 create_new: bool = False,
                 overwrite: bool = False):
        """Default constructor for a dir object

        Args:
            name (str): name or path of a dir on OS
            create_new (bool): Flag to allow creation of dir if not exists
            overwrite (bool): Overwrites if already exiats

        """
        super(AbstractDirDriver, self).__init__(name)
        self.__create_new_flag = create_new
        self._overwrite = overwrite
        self._exists = False
        self._full_path = None

    def get_handle(self):
        """Returns handle to file or directory to perform other IO operations

        """
        return self._full_path

    @property
    def name(self) -> str:
        """Name property of an IO object

        """
        return self._name

    @name.setter
    def name(self, value):
        """Name property of a directory

        """
        self._name = validFileName(value, initCap=False).decode('utf8')

    @property
    def full_path(self):
        """full path of directory

        """
        if self._full_path is None:
            if self._name is not None:
                self._full_path = pathlib.Path(self._name).absolute()
        return self._full_path

    @property
    def exists(self):
        """Check whether file exists or not

        """
        if self._full_path is None:
            return False
        else:
            return pathlib.os.path.exists(self._full_path)

    def copy(self, destination, force=False, create_path=False):
        """Copy dir to new location passed as param. If dir already exists \
                and force param is True, it will overwrite the destination \
                dir else will return with no operation.

        Args:
            destination (str): The target location where dir needs to be copied
            force (bool): If set to True, it will overwrite the dir in \
                    destination
            create_path (bool): create the destination path if not exists

        Returns:
            file_path (pathlib.Path): Returns an instance of :class:`Path` \
                    if dir copied else None

        """
        raise NotImplementedError('This is an abstract method and can'
                                  't be\
                                  called from instance variable')

    def move(self, destination, force=False, create_path=False):
        """Moves the dir to the destination. Please see :meth:`copy` \
                for more information on arguments

        """
        raise NotImplementedError('This is an abstract method and can'
                                  't be\
                                  called from instance variable')

    def list_all(self, pattern: str = None) -> str:
        """Return all files and folders available under current directory

        Args:
            pattern (str): wild card pattern used to search files or folders

        """
        raise NotImplementedError('This is an abstract method and can'
                                  't be\
                                  called from instance variable')

    def list_files(self, pattern: str = None) -> Type[List[pathlib.Path]]:
        """Returns an list of files in current directory. If pattern is not\
        none, filters out files from the list

        Args:
            pattern (str): Filter out the files based on pattern provided

        """
        raise NotImplementedError('This is an abstract method and can'
                                  't\
                                  be called from instance variable')

    def list_directories(self,
                         pattern: str = None) -> Type[List[pathlib.Path]]:
        """Returns an list of directories in current directory. If pattern is not\
        none, filters out directories from the list

        Args:
            pattern (str): Filter out the dirs based on pattern provided

        """
        raise NotImplementedError('This is an abstract method and can'
                                  't\
                                  be called from instance variable')


class AbstractFileDriver(AbstractDirDriver):
    """An abstract file representing an file on OS

    """

    def __init__(self,
                 name: str = None,
                 repo_details: Type[Dict] = None,
                 create_new: bool = False,
                 base_path: Type[pathlib.Path] = None,
                 overwrite: bool = False):
        """Default constructor of an file object

        """
        super(AbstractFileDriver, self).__init__(name, repo_details,
                                                 create_new, overwrite)
        self._base_path = base_path
        self._content = None
        self._size = -1
        self._base_name = None
        self._ext = None

    @property
    def name(self) -> str:
        """Name property of an IO object

        """
        return self._name

    @name.setter
    def name(self, value):
        """Name property of an file and derives basename and extension \
                properties from this name

        """
        self._name = validFileName(value, initCap=False).decode('utf8')
        _file_name = self._name
        if _file_name.rfind(os.path.sep) >= 0:
            _file_name = _file_name[(_file_name.rindex(os.path.sep) + 1):]
        if _file_name.rfind('.') >= 0:
            self._base_name = _file_name[0:_file_name.rindex('.')]
            self._ext = _file_name[(_file_name.rindex('.') + 1):]
        else:
            self._base_name = _file_name
            self._ext = None

    @property
    def base_path(self):
        """Base or Parent path of an file

        """
        if self._base_path is None:
            if self._name is not None:
                _temp_path = pathlib.Path(self._name)
                _temp_path = pathlib.Path(_temp_path.parent)
                return _temp_path.absolute()
        return self._base_path

    @base_path.setter
    def base_path(self, value):
        if pathlib.os.path.exists(value):
            value = pathlib.Path(value)
            if str(value).find('~') >= 0:
                self._base_path = pathlib.Path(value).expanduser()
            else:
                self._base_path = pathlib.Path(value).absolute()
        else:
            self._base_path = None

    @property
    def base_name(self):
        """The part before the dot of file name

        """
        return self._base_name

    @property
    def ext(self):
        """Extension part of filename

        """
        return self._ext

    @property
    def size(self):
        """Size of file

        """
        if self._size <= 0:
            self._size = self.full_path.lstat.size
        return self._size

    @property
    def content(self):
        """Content of a file on filesystem in bytes

        """
        return self._content

    @property
    def full_path(self):
        """full path to file including name and extension

        """
        if self._full_path is None:
            if self.base_path is not None:
                self._full_path = self.base_path.joinpath(
                    self._name).absolute()
        return self._full_path

    @property
    def exists(self):
        """Check whether file exists or not

        """
        if self._full_path is None:
            return False
        return self._full_path.exists()


class AbstractPackageFileDriver(AbstractFileDriver):
    """An abstract class of an physical package file

    """

    def __init__(self,
                 name: str = None,
                 repo_details: Type[Dict] = None,
                 create_new: bool = False,
                 base_path: Type[pathlib.Path] = None,
                 overwrite: bool = False):
        """Default constructor of an package file

        """
        super(AbstractPackageFileDriver, self).__init__(
            self, name, repo_details, create_new, base_path, overwrite)

    def extract_to(self,
                   target_path: str,
                   name_as_sub_folder: bool = True,
                   overwrite: bool = False) -> (Type[F], str):
        """Extract the contents of package to the specified path

        Args:
            target_path (str): path to the lication where package needs to be extracted
            name_as_sub_folder (bool): creates a sub folder under target_path with the\
                    same name as package file name before extracting contents. Default value is True
            overwrite (bool): Overwrites the contents if already exists in target location

        """
        pass


class AbstractScriptFileDriver(AbstractFileDriver):
    """An abstract class for an script file on filesystem

    """

    def __init__(self,
                 name: str,
                 repo_details: Type[Dict] = None,
                 create_new: bool = False,
                 base_path: Type[pathlib.Path] = None,
                 overwrite: bool = False,
                 arg_list: Type[Dict] = None):
        """Default constructor for an script file

        """
        super(AbstractScriptFileDriver, self).__init__(
            name, repo_details, create_new, base_path, overwrite)
        self._args_list_for_script = arg_list

    def get_script_path(self) -> str:
        """Returns the script name on the file system

        """
        return self.full_path

    def get_args_list_for_script(self) -> Type[List]:
        """Returns an list of arguments that needs to be passed to script for execution

        """
        pass

    def get_stdout_pipe(self) -> Any:
        """Returns an instance of process Pipe for stdout

        """
        pass

    def get_stderr_pipe(self) -> Any:
        """Returns an instance of process Pipe for stderr

        """
        pass

    def get_process_instance(self) -> Any:
        """Returns an instance of process that will be execute the script

        """
        pass

    def execute_script(self) -> (Type[F], str):
        """Executes the script along with the parameters provided in setup conf

        """
        pass
