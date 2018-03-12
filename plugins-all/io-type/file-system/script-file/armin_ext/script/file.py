"""
.. module:: file
   :platform: Unix, Windows
   :synopsis: represents an script file on fs

.. moduleauthor:: Ajeet Singh <singh.ajeet@gmail.com>
"""
from pathlib import Path
from subprocess import Popen, PIPE
from typing import Type, Dict, Any
from configparser import ConfigParser
from armin.api.managers.io.interface import AbstractScriptFileDriver
from armin.api.share.constants import v_PC, F


class ScriptFileDriver(AbstractScriptFileDriver):
    """Represents a physical script file.\
    """

    def __init__(self, name: str, repo_details: Type[Dict], create_new: bool=False, base_path: str=None, overwrite: str=False, arg_list: Type[Dict]=None):
        """Default constructor of script file
        """
        super(ScriptFileDriver, self).__init__(name, repo_details, create_new, base_path, overwrite, arg_list)
        #Init other attribs
        self._process = None
        self._std_out_pipe = None
        self._std_err_pipe = None
        self._allowed_setup_file_ext = v_PC.ALLOWED_SCRIPT_EXT
        if self.ext is None or self.ext not in self._allowed_setup_file_ext:
            raise Exception('Unknown setup file format. Only following formats are allowed %s' % self._allowed_setup_file_ext)
        if create_new is False and not self.exists:
            raise Exception('Unable to find script file')

    def get_script_path(self) -> str:
        """Returns the name of the script
        """
        return self.full_path

    def get_args_list_for_script(self) -> Type[Dict]:
        """Returns an list containing the args to be passed to setup script
        """
        return self._args_list_for_script

    def get_stdout_pipe(self) -> Any:
        """Returns an instance of std out pipe
        """
        return self._std_out_pipe

    def get_stderr_pipe(self) -> Any:
        """Returns an instance of std err pipe
        """
        return self._std_err_pipe

    def get_process_instance(self):
        """Returns an instance of process used to execute script
        """
        return self._process

    def execute_script(self) -> (Type[F], str):
        """Executes the setup script and returns the results for same
        """
        if self._args_list_for_script is None:
            self._args_list_for_script = []
        if self._args_list_for_script.count() > 0:
            self._process = Popen([self.full_path, self._args_list_for_script], stdout=PIPE, stderr=PIPE)
        if self._args_list_for_script.count <= 0:
            self._process = Popen(self.full_path, stdout=PIPE, stderr=PIPE)
        (self._std_out_pipe, self._std_err_pipe) = self._process.communicate()
        if self._std_err_pipe is not None and len(self._std_err_pipe) > 0:
            return (F.FAILED ,'Error while executting script: %s' % self._std_err_pipe)
        return (F.SUCCESS, self._std_out_pipe)
