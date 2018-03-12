"""
.. module:: source_driver
   :platform: Unix, Windows
   :synopsis: A default implementation of source system driver
"""
from typing import Type, Dict, Any
import pathlib
from armin.api.share.constants import N, F, V
from tinydb import TinyDB, Query


def get_meta_table(meta_repo_details:Type[Dict]):
    """Returns the table from meta repo based on details passed as args
    """
    __db_path = meta_repo_details[N.DB_URI]
    if __db_path.find('~') >= 0:
        __db_path = pathlib.Path(__db_path).expanduser()
    else:
        __db_path = pathlib.Path(__db_path).absolute()
    __meta_db = TinyDB(__db_path)
    if __meta_db is None:
        return (F.FAILED, 'Unable to create instance of TinyDB')
    __source_sys_meta_table = __meta_db\
                .table(meta_repo_details[N.META_TABLE])
    if __source_sys_meta_table is None:
        return (F.FAILED, 'Inconsistent meta repo. Can not find source\
                system details table - %s' % meta_repo_details[N.META_TABLE])
    else:
        return (F.SUCCESS, __source_sys_meta_table)

def connect_to_meta(meta_repo_details:Type[Dict], name:str) -> (Type[F], Any):
    """Connect to metadata database using the details provided asparameters in the constructor
    Args:
        meta_repo_details (Dict): Repository details for making connection and query
        name (str): Name of the item that needs to be queried
        Returns:
            status (Tuple): Returns flag Success or Failed and details in case of failure and table record in case of success
        """
    __record = None
    (status, result_obj) = get_meta_table(meta_repo_details)
    if status == F.SUCCESS:
        __source_sys_meta_table = result_obj
        __record = __source_sys_meta_table\
                .get(Query()[N.NAME] == name)
    else:
        return (status, result_obj)
    if __record is not None:
        return (F.SUCCESS, __record)
    return (F.FAILED, 'Record not found in meta repo')
