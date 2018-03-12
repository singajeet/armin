"""
.. module:: template
   :platform: Any
   :synopsis: A default model of an package
.. moduleauthor:: Ajeet Singh <singajeet@gmail.com>
"""
import tempfile
import pathlib
import os
from typing import Type, Dict, List
from configparser import ConfigParser
from tinydb import Query
from armin.api.managers.package.interface import AbstractPackage
from armin.api.share import utils
from armin.api.share.constants import N, F, v_PC


class Package(AbstractPackage):
    """A default package template in the package mgmt
    """

    def __init__(self, name:str, repo_details:Type[Dict]):
        """Default constructor
        """
        super(Package, self).__init__(name, repo_details)

    def connect_to_meta(self) -> (Type[Dict], str):
        """Connect to meta repo and loads the details if available
        """
        (status, __result) = utils.connect_to_meta(self._repo_details, self._name)
        if status == F.SUCCESS:
            self._meta = __result
            return (F.SUCCESS, '')
        return (status, __result)

    def _prepare_temp_workspace(self):
        """Prepares an temp dir/workspace to be used by this package
        """
        if self._meta is not None and self._meta.__contains__(N.TEMP_WORKSPACE):
            _wrk_space = self._meta[N.TEMP_WORKSPACE]
            if _wrk_space is not None:
                if os.path.exists(_wrk_space):
                    return
        self._meta[N.TEMP_WORKSPACE] = tempfile.mkdtemp(prefix='package', suffix=self._name)
        return

    def get_setup_config(self) -> Type[ConfigParser]:
        """Returns the config file available in this packe
        """
        __module_path = os.path.relpath(__file__)
        __module_path = pathlib.Path(__module_path)
        if os.name == 'posix':
            __config_path = __module_path.joinpath('setup.ini')
        else:
            __config_path = __module_path.joinpath('setup.ini')
        __config_path = __config_path.absolute()
        __package_config = ConfigParser()
        __package_config.read(__config_path)
        return __package_config

    def get_setup_script_args(self) -> Type[List]:
        """Returns the args required by setup script
        """
        return self.get_setup_config().get(v_PC.SETUP_SECTION_KEY, v_PC.ARG_LIST_FOR_SCRIPT_KEY)

    def get_setup_script_path(self) -> str:
        __module_path = os.path.relpath(__file__)
        __module_path = pathlib.Path(__module_path)
        __script_path = __module_path.joinpath(self.get_setup_config().get(v_PC.SETUP_SECTION_KEY, v_PC.SETUP_FILE_KEY))
        __script_path = pathlib.Path(__script_path).absolute()
        return __script_path

    def save(self) -> (Type[F], str):
        """Saves the meta data in the configured repo
        """
        (status, __meta_table) = utils.get_meta_table(self._repo_details)
        if status == F.SUCCESS:
            record = __meta_table.get(Query()[N.NAME] == self._name)
            if record is not None and len(record) > 0:
                __meta_table.update({N.DETAILS: self._meta}, N.NAME == self._name)
            else:
                __meta_table.insert({N.NAME: self._name, N.DETAILS: self._meta,\
                                     N.MARKED_FOR_DELETION: False, N.DELETION_TYPE: F.NONE})
            return (F.SUCCESS, 'Meta data has been saved successfully!')
        else:
            return (F.FAILED, 'Unable to find meta table for setup scripts')

    def remove(self, hard:bool=False) -> (Type[F], str):
        """Removes the package template info from the metadata repo. if arg 'hard' is True,\
        it deletes the whole template from the filesystem as well
        Args:
        hard (bool): If true, removes the template from filesystem also else remove meta data
        only
        """
        (status, __meta_table) = utils.get_meta_table(self._repo_details)
        if status == F.SUCCESS:
            record = __meta_table.get(Query()[N.NAME] == self._name)
            if record is not None and len(record) > 0:
                __meta_table.update({N.MARKED_FOR_DELETION: True,\
                                     N.DELETION_TYPE: F.SOFT}, [N.NAME] == self._name)
                if hard is True:
                    __meta_table.update({N.DELETION_TYPE: F.HARD}, [N.NAME] == self._name)
                return (F.SUCCESS, 'Package Template soft deleted from meta repo')
            else:
                return (F.FAILED, 'No such package template exists in meta repo: %s' % self._name)
        else:
            return (F.FAILED, 'Unable to locate meta table: %s' % self._repo_details[N.META_TABLE])

    def set_meta(self, namespace:str=None, entry_point:Type[Dict]=None,\
                 description:str=None, crc:str=None, author:str=None,\
                 company:str=None, url:str=None) -> Type[F]:
        """Set the value of meta data attributes for those which are passed\
        as arguments
        """
        if namespace is not None:
            self._meta[N.NAMESPACE] = namespace
        if entry_point is not None:
            self._meta[N.ENTRY_POINT] = entry_point
        if description is not None:
            self._meta[N.DESCRIPTION] = description
        if crc is not None:
            self._meta[N.CRC] = crc
        if author is not None:
            self._meta[N.AUTHOR] = author
        if company is not None:
            self._meta[N.COMPANY] = company
        if url is not None:
            self._meta[N.URL] = url
        self.save()
