"""
.. module:: file
   :platform: Unix, Windows
   :synopsis: represents an package file on file-system

.. moduleauthor:: Ajeet Singh <singh.ajeet@gmail.com>
"""
import os
from typing import Type, Dict, Type
from goldfinch import validFileName
from pathlib import Path
import pathlib
import zipfile
import io
import shutil
from armin.api.managers.io.interface import AbstractPackageFileDriver


class PackageFileDriver(AbstractPackageFileDriver):
    """Represents a physical package file in the package management system.\
            This class supports 3 commands...

            * copy
            * move
            * extract_to
    """

    def __init__(self, name: str, repo_details: Type[Dict],\
                 create_new: bool=False, base_path: Type[Path]=None,\
                 overwrite: bool=False):
        """Default constructor of package file
        """
        super(PackageFileDriver, self).__init__(name, repo_details, create_new,\
                                          base_path, overwrite)
        if create_new is False:
            if self.exists:
                if not zipfile.is_zipfile(self.full_path):
                    raise Exception('Not a valid zip file')

    def extract_to(self, target_path, name_as_sub_folder=True, overwrite=False):
        """Extract the contents of package to the specified path

        Args:
            target_path (str): path to the lication where package needs to be extracted
            name_as_sub_folder (bool): creates a sub folder under target_path with the\
                    same name as package file name before extracting contents.\
                    Default value is True
            overwrite (bool): Overwrites the contents if already exists in target location
        """
        if target_path is not None and target_path.find('~') >= 0:
            dest_path = pathlib.Path(target_path).expanduser()
        elif target_path is not None:
            dest_path = pathlib.Path(target_path).absolute()
        else:
            raise Exception('Can''t accept blank for destination path')
        if dest_path.exists():
            if name_as_sub_folder is True:
                dest_path = dest_path.joinpath(self.base_name).absolute()
                if not dest_path.exists():
                    dest_path.mkdir(parents=True)
            else:
                if overwrite is True:
                    for f in dest_path.iterdir():
                        if f.is_dir():
                            shutil.rmtree(f)
                        else:
                            f.unlink()
            if len(self.content) > 0:
                file_bytes = io.BytesIO(self.content)
                zippedfile = zipfile.ZipFile(file_bytes)
                zippedfile.extractall(dest_path)
            return dest_path
        else:
            raise Exception('Invalid destination path specified')
