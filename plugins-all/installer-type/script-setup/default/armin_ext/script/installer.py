"""
.. module:: file
   :platform: Unix, Windows
   :synopsis: represents an script file on fs

.. moduleauthor:: Ajeet Singh <singh.ajeet@gmail.com>
"""
from pathlib import Path
from subprocess import Popen, PIPE
from typing import Type, Dict, Type
from configparser import ConfigParser
from armin.api.managers.io.interface import AbstractScriptFileDriver
from armin.api.share.constants import v_PC, F


class ScriptFileDriver(AbstractScriptFileDriver):
    """Represents a physical script file.\
    """

    def __init__(self, package_path: str, repo_details: Type[Dict]):
        """Default constructor of script file
        """
        #Read config file first to get setup file name and other attrs
        self.__setup_config_path = None
        if package_path.find('~') >= 0:
            self.__setup_config_path = Path(package_path).expanduser()
            self.__setup_config_path = self.__setup_config_path.joinpath('setup.ini')
            self.__setup_config_path = self.__setup_config_path.absolute()
        else:
            self.__setup_config_path = Path(package_path).joinpath('setup.ini')
            self.__setup_config_path = self.__setup_config_path.absolute()
        if not self.__setup_config_path.exists():
            raise Exception('Unable to locate setup config')
        self.__config = ConfigParser()
        self.__config.read(self.__setup_config_path)
        self.__setup_file_name = self.__config.get(v_PC.SETUP_SECTION_KEY, v_PC.SETUP_FILE_KEY)
        #call super constructor with the setup_file_name and package_path as its args
        super(PackageSetupFileDriver, self).__init__(self.__setup_file_name, repo_details, False, package_path, False)
        #Init other attribs
        self.__allowed_setup_file_ext = v_PC.ALLOWED_SCRIPT_EXT
        self.__args_list_for_script = list(self.__config.get(v_PC.SETUP_SECTION_KEY, v_PC.ARG_LIST_FOR_SCRIPT_KEY))
        if self.ext is None or self.ext not in self.__allowed_setup_file_ext:
            raise Exception('Unknown setup file format. Only following formats are allowed %s' % self.__allowed_setup_file_ext)
        if not self.exists:
            raise Exception('Unable to find setup file in current package')

    def get_script_name(self):
        """Returns the name of the script
        """
        return self.name

    def get_args_list_for_script(self):
        """Returns an list containing the args to be passed to setup script
        """
        return self.__args_list_for_script

    def execute_script(self):
        """Executes the setup script and returns the results for same
        """
        _process = Popen([self.name, self.__args_list_for_script], stdout=PIPE, stderr=PIPE)
        (_stdout, _stderr) = _process.communicate()
        if _stderr is not None:
            return (F.FAILED ,'Error while executting setup script: %s' % _stderr)
        return (F.SUCCESS, _stdout)
