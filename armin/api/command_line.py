"""
.. module:: command_line
   :platform: Any
   :synopsis: Command line interface to Armin Studio
.. moduleauthor: Ajeet Singh <singajeet@gmail.com>

"""
from armin.api.managers.source.manager import SourceDriverManager
from armin.api.managers.io.manager import FileSystemManager



def main(*args, **kwargs):
    """Main entry point to the Armin Studio
    
    """
    src_mgr = SourceDriverManager()
    fs_mgr = FileSystemManager()
