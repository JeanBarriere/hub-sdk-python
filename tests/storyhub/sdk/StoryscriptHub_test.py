# -*- coding: utf-8 -*-
import tempfile
from time import sleep

from storyhub.sdk.StoryscriptHub import StoryscriptHub
from storyhub.sdk.GraphQL import GraphQL
from storyhub.sdk.db.Service import Service
from storyhub.sdk.service.ServiceData import ServiceData
from tests.storyhub.sdk.JsonFixtureHelper import JsonFixtureHelper


class VerifiableService:
    def __init__(
        self, name: str, description: str, uuid: str, configuration: dict,
    ):
        self.name = name
        self.description = description
        self.uuid = uuid
        self.configuration = configuration

    def verify(self, service: ServiceData):
        assert service.name() == self.name
        assert service.description() == self.description
        assert service.uuid() == self.uuid
        assert (
            service.configuration().actions()[0].name()
            == list(self.configuration["actions"].keys())[0]
        )


def test_caching(mocker):
    config = {"actions": {"foo": "bar"}}

    actual_service = VerifiableService(
        name="sample_name",
        description="service_description",
        uuid="A86742FD-55B4-4AEC-92B9-9989B3AF2F7E",
        configuration=config,
    )

    registered_services = [actual_service]

    mocker.patch.object(GraphQL, "get_all", return_value=registered_services)
    hub = StoryscriptHub(db_path=tempfile.mkdtemp())
    # No need to call update_cache explicitly, since the background thread will
    # call it. Just sleep for a split second.
    # hub.update_cache()
    sleep(0.2)
    assert hub.get_all_service_names() == [
        "sample_name",
    ]

    service = hub.get(name="sample_name")
    actual_service.verify(service)

    second_service = VerifiableService(
        name="second_service",
        description="second_service_description",
        uuid="7D5D5A94-F45D-4F44-9B65-BAE13C49AAF4",
        configuration=config,
    )
    registered_services.append(second_service)

    actual_service = hub.get(name="second_service")

    assert actual_service is not None


def test_get_with_name(mocker):
    hub = StoryscriptHub(db_path=tempfile.mkdtemp())
    mocker.patch.object(Service, "select")

    assert hub.get("redis") is not None

    Service.select().where.assert_called_with((Service.name == "redis"))


not_python_fixture = JsonFixtureHelper.load_fixture("not_python_fixture")


def test_service_wrapper(mocker):
    hub = StoryscriptHub(db_path=tempfile.mkdtemp())

    mocker.patch.object(GraphQL, "get_all", return_value=[not_python_fixture])

    mocker.patch.object(ServiceData, "from_dict")

    assert hub.get("not_python") is not None

    ServiceData.from_dict.assert_called_with(
        data={"service_data": not_python_fixture}
    )


def test_get_with_wrap_service(mocker):
    hub = StoryscriptHub(db_path=tempfile.mkdtemp())

    mocker.patch.object(GraphQL, "get_all", return_value=[not_python_fixture])

    mocker.patch.object(ServiceData, "from_dict")

    assert hub.get("not_python") is not None

    ServiceData.from_dict.assert_called_with(
        data={"service_data": not_python_fixture}
    )
