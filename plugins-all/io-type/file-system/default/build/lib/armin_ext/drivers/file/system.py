"""
.. module:: system
   :platform: Any
   :synopsis: Generic driver classes for file systems
.. moduleauthor:: Ajeet Singh
"""
import pathlib
import shutil
from typing import Type, Dict
from armin.api.managers.io.interface import AbstractFileDriver, AbstractDirDriver


class FileDriver(AbstractFileDriver):
    """Represents a file on file system. This class supports :meth:`copy` \
            and :meth:`move` commands only and for all other operations use \
            :mod:`os` or :mod:`pathlib` modules. There are two attributes \
            :attr:`os` and :attr:`path` which provides access to both of the \
            above mentioned modules respectively

    """

    def __init__(self,
                 name: str,
                 repo_details: Type[Dict] = None,
                 create_new: bool = False,
                 base_path: str = None,
                 overwrite: bool = False):
        """Default constructor of an file

        """
        super(FileDriver, self).__init__(name, repo_details, create_new,
                                         base_path, overwrite)
        self.__src_file = None
        if name is None:
            raise Exception('Filename can' 't have blank')
        if base_path is None:
            if name.find('~') >= 0:
                self.__src_file = pathlib.Path(name).expanduser()
            else:
                self.__src_file = pathlib.Path(name).absolute()
        else:
            if base_path.find('~') >= 0:
                self.__src_file = pathlib.Path(
                    base_path).expanduser().joinpath(name).absolute()
            else:
                self.__src_file = pathlib.Path(base_path).absolute().joinpath(
                    name).absolute()
        if create_new == False:
            self._open(name, base_path)
        else:
            self._create(name, base_path, overwrite)

    def _create(self,
                name: str,
                base_path: str = None,
                overwrite: bool = False):
        """Creates a new file and overwrites an existing one if overwrite param is True

        """
        if self.__src_file.exists():
            if overwrite is True:
                self.__src_file.unlink()
                self.__src_file.touch()
            else:
                raise Exception(
                    'A file with same name and parent already exists')
        else:
            self.__src_file.touch()
        self._open(name, base_path)

    def _open(self, name: str, base_path: str = None):
        """Opens and read file contents if exists

        """
        if self.__src_file.exists():
            self.name = self.__src_file.name
            self.base_path = self.__src_file.parent.absolute()
            self._content = self.__src_file.read_bytes()
            self._exists = True
            self._size = self.__src_file.stat().st_size
            self._full_path = self.__src_file.absolute()
        else:
            raise Exception('Invalid file provided')

    def copy(self, destination, force=False, create_path=False):
        """Copy file to new location passed as param. If file already exists and\
        force param is True, it will overwrite the destination file else will\
        return with no operation.

        Args:
            destination (str): The target location where file needs to be copied
            force (bool): If set to True, it will overwrite the file in destination
            create_path (bool): create the destination path if not exists

        Returns:
            file_path (pathlib.Path): Returns an instance of :class:`Path`\
        if file copied else None

        """
        if destination is not None and destination.find('~') >= 0:
            dest_path = pathlib.Path(destination).expanduser()
        elif destination is not None:
            dest_path = pathlib.Path(destination).absolute()
        else:
            raise Exception('Invalid path provided - %s' % dest_path)
        if dest_path.exists():
            if dest_path.is_dir():
                dest_file = dest_path.joinpath(self.name)
                if dest_file.exists() and force == True:
                    dest_file.unlink()
                    dest_file.write_bytes(self.content)
                    return dest_file
                elif dest_file.exists() and force == False:
                    return None
                else:
                    dest_file.write_bytes(self.content)
                    return dest_file
            else:
                dest_file = pathlib.Path(dest_path)
                if force == True:
                    dest_file.unlink()
                    dest_file.write_bytes(self.content)
                    return dest_file
                else:
                    return None
        elif create_path == True:
            dest_path = dest_path.mkdir(parents=True)
            dest_file = dest_path.joinpath(self.name)
            dest_file.write_bytes(self.content)
            return dest_file
        else:
            raise Exception('Invalid destination path')

    def move(self, destination, force=False, create_path=False):
        """Moves the current file to the destination. Please see :meth:`copy` \
        for more information on arguments

        """
        new_file = self.copy(destination, force, create_path)
        if new_file is not None:
            if new_file.exists():
                old_file = pathlib.Path(self.base_path).joinpath(self.name)
                self.base_path = new_file.parent.absolute()
                old_file = pathlib.Path(old_file)
                old_file.unlink()
                return new_file
        return None


class DirectoryDriver(AbstractDirDriver):
    """Same as :class:`File` but works on dirs instead

    """

    def __init__(self,
                 name: str,
                 repo_details: Type[Dict] = None,
                 create_new: bool = False,
                 overwrite: bool = False):
        """Default constructor for an directory

        """
        super(Directory, self).__init__(name, repo_details, create_new,
                                        overwrite)
        dir_path = pathlib.Path(name)
        if dir_path.exists():
            self._full_path = dir_path.absolute()
        else:
            if create_new is True:
                dir_path = dir_path.absolute()
                self._full_path = dir_path.mkdir(parents=True)
            else:
                raise Exception('Invalid path provided! Use "create_new" to \
                                create new directory')

    def copy(self,
             destination: str,
             force: bool = False,
             create_path: bool = False) -> Type[pathlib.Path]:
        """Copy file to new location passed as param. If file already exists \
                and force param is True, it will overwrite the destination \
                file else will return with no operation.

        Args:
            destination (str): The target location where file needs to be copied
            force (bool): If set to True, it will overwrite the file in \
                    destination
            create_path (bool): create the destination path if not exists

        Returns:
            file_path (pathlib.Path): Returns an instance of \
                    :class:`Path` if file copied else None

        """
        if destination is not None and destination.find('~') >= 0:
            dest_path = pathlib.Path(destination).expanduser()
        elif destination is not None:
            dest_path = pathlib.Path(destination).absolute()
        else:
            raise Exception('Invalid path provided - %s' % dest_path)
        if dest_path.exists():
            if dest_path.is_dir():
                if force is True:
                    dest_path = pathlib.Path(dest_path).absolute()
                    shutil.rmtree(dest_path)
                    shutil.copytree(self.full_path, dest_path)
                    return dest_path
                else:
                    raise Exception('Destination path already exists. \
                                    Use "force" param to overwrite')
            elif dest_path.is_file():
                raise Exception('Destination provided is a file')
        else:
            parent_path = dest_path.parent
            if parent_path.exists():
                shutil.copytree(self.full_path, dest_path)
            else:
                if create_path is True:
                    parent_path.mkdir(parents=True)
                    shutil.copytree(self.full_path, dest_path)
                else:
                    raise Exception('Provided path doesn''t exist - %s' \
                                    % parent_path)
        return None

    def move(self,
             destination: str,
             force: bool = False,
             create_path: bool = False) -> Type[pathlib.Path]:
        """Moves the current dir to the destination. \
                Please see :meth:`copy` for more information on arguments

        """
        new_dir = self.copy(destination, force, create_path)
        if new_dir is not None:
            if new_dir.exists():
                old_dir = pathlib.Path(self.full_path)
                self.full_path = new_dir.absolute()
                shutil.rmtree(old_dir)
                return new_dir
        return None

    def list_all(self, pattern=None):
        """List all files and folders if available

        """
        if self.full_path is not None:
            if pattern is None:
                return self.full_path.glob('*')
            else:
                return self.full_path.glob(pattern)
        else:
            return None

    def list_files(self, pattern=None):
        """List all files in directory matching the passed pattern

        """
        if self.full_path is not None:
            if pattern is None:
                return [f for f in self.full_path.glob('*') if f.is_file()]
            else:
                return [f for f in self.full_path.glob(pattern) if f.is_file()]
        else:
            return None

    def list_directories(self, pattern=None):
        """List all dirs in directory matching the passed pattern

        """
        if self.full_path is not None:
            if pattern is None:
                return [f for f in self.full_path.glob('*') if f.is_dir()]
            else:
                return [f for f in self.full_path.glob(pattern) if f.is_dir()]
        else:
            return None
