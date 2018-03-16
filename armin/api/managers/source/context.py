"""
.. module:: context
   :platform: Any
   :synopsis: async context manager implementation for source driver
.. moduleauthor:: Ajeet Singh <singajeet@gmail.com>
"""
from async_generator import asynccontextmanager
from typing import Type, Any, Dict
from armin.api.share.constants import V, F, N


@asynccontextmanager
async def source_driver(loop: Any, url: str=None, inputs: Type[Dict]=None,\
                        task: str=None, expected_result_type: Type[V]=V.JSON):
    """Function to connect, execute task, download result and cleanup connection to source system using context manager

    Examples:
            >>> from armin.api.managers.source import web
            >>> from armin.api.share.constants import V
            >>> url = 'http://<url to source>'
            >>> task = 'download'
            >>> inputs = {'package': 'mypackage',
                          'version': '1.0',
                         }
            >>> expected_result_type = V.FILE
            >>> with web.source_driver(url, inputs, task, expected_result_type) as resp:
                    with open('download.txt') as file:
            ...         file.write(resp.read())

    Args:
        url (str): Url to the source system. Need to provide port if not\
    running on default 80 port
        inputs (dict): key-value paired inputs to source as dict
        task (str): name of the task provided by source system
        expected_result_type (V): expected result type constant, eg., V.JSON, V.FILE, ETC

    Return:
            An instance of class `aiohttp.Response`

    """
    from armin.api.managers.source.manager import SourceDriverManager
    from armin.api.share.constants import F, V
    import asyncio
    manager = SourceDriverManager()
    (status, message) = manager.load_driver()
    if status == F.SUCCESS:
        (status, driver) = manager.get_source_system_driver()
        if status == F.SUCCESS:
            driver.connect_to_meta()
            if loop is not None:
                driver.prepare_to_connect(loop)
            else:
                loop = asyncio.get_event_loop()
                driver.prepare_to_connect(loop)
            if url is not None:
                driver.set_meta(url=url)
            resp=None
            if inputs is not None:
                driver.put_input(inputs)
            if task is not None:
                resp = await driver\
                        .perform_task(task=task,\
                                      expected_result_type=expected_result_type)
                yield resp
            else:
                resp = await driver\
                        .perform_task(expected_result_type=expected_result_type)
                yield resp
            resp.close()
