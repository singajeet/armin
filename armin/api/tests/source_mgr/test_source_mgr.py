"""
.. module: Test cases for SourceDriverManager
   :platform: Any
   :synopsis: Test cases for SourceDriverManager
"""
import pytest
import pkg_resources
from armin.api.share.constants import F, V


@pytest.fixture(scope="module")
def source_manager_instance(request):
    """Fixture for creating SourceDriverManager instance

    """
    from armin.api.managers.source.manager import SourceDriverManager
    manager = SourceDriverManager()

    def teardown_mgr():
        """Will be called once all tests completes

        """
        print('Finalizing Driver Manager...')

    request.addfinalizer(teardown_mgr)
    return manager


@pytest.fixture(scope="module")
def source_driver_instance(request, source_manager_instance):
    """Fixture to provide instance of Driver

    """
    source_manager_instance.load_driver()
    result = source_manager_instance.get_source_system_driver()

    def teardown_drv():
        print('Finalizing Driver...')
        import asyncio
        loop = asyncio.get_event_loop()
        loop.run_until_complete(
            asyncio.gather(result[1]._DefaultSourceDriver__session.close()))

    request.addfinalizer(teardown_drv)
    return result[1]


def test_source_driver_installed_count():
    """Counts the number of drivers installed of type Source Driver

    """
    drivers_list = [
        drv for drv in pkg_resources.iter_entry_points('source.drivers')
    ]
    assert len(drivers_list) == 1, "Source Drivers count should be 1 only"


def test_source_driver_name():
    """Test the name of the installed source system driver

    """
    drivers_list = [
        drv for drv in pkg_resources.iter_entry_points('source.drivers')
    ]
    assert drivers_list[0].name == 'default_driver'


def test_SourceDriverManager_init(source_manager_instance):
    """Tests the SourceDriverManager() instance creation

    """
    assert source_manager_instance is not None


def test_SourceDriverManager_load_driver(source_manager_instance):
    """Test method load_driver() of SourceDriverManager

    """
    result = source_manager_instance.load_driver()
    assert result[0] == F.SUCCESS


def test_SourceDriverManager_get_source_system_driver(source_manager_instance):
    """Test method get_source_system_driver() of SourceDriverManager

    """
    result = source_manager_instance.get_source_system_driver()
    assert result[0] == F.SUCCESS
    assert result[1]._name == 'default_driver'


def test_DefaultSourceDriver_connect_to_meta(source_driver_instance):
    """Test method connect_to_meta of DefaultSourceDriver

    """
    result = source_driver_instance.connect_to_meta()
    assert result[0] == F.SUCCESS


def test_DefaultSourceDriver_connect_and_list(source_driver_instance):
    """Test method prepare_to_connect

    """
    import asyncio
    loop = asyncio.get_event_loop()
    assert loop is not None
    source_driver_instance.prepare_to_connect(loop)
    assert source_driver_instance._DefaultSourceDriver__session is not None
    source_driver_instance.set_meta(task='index')
    source_driver_instance.set_meta(url='http://localhost:8000/package')
    loop.run_until_complete(
        asyncio.gather(source_driver_instance.perform_task()))
    temp_result = loop.run_until_complete\
            (asyncio.gather(source_driver_instance.get_output()))
    (status, result) = temp_result[0]
    assert status == F.SUCCESS
    assert type(result) == dict


def test_DefaultSourceDriver_connect_and_download(source_driver_instance):
    """Test method prepare_to_connect

    """
    import asyncio
    from armin.api.managers.io.interface import AbstractFileDriver
    loop = asyncio.get_event_loop()
    assert loop is not None
    source_driver_instance.prepare_to_connect(loop)
    assert source_driver_instance._DefaultSourceDriver__session is not None
    source_driver_instance._details.pop('TEMP_FILE')
    source_driver_instance.set_meta(
        url='http://localhost:8000/downloads/package1.pkg')
    loop.run_until_complete(
        asyncio.gather(
            source_driver_instance.perform_task(expected_result_type=V.FILE)))
    #print('Session: %s' % (source_driver_instance._DefaultSourceDriver__session is not None))
    #assert source_driver_instance._DefaultSourceDriver__session is not None
    result = loop.run_until_complete\
            (asyncio.gather(source_driver_instance.get_output()))
    #print(result)
    (status, result) = result[0]
    assert status == F.SUCCESS
    assert isinstance(result, AbstractFileDriver)
