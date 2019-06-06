import json

from storyscript.hub.sdk.service.Contact import Contact
from storyscript.hub.sdk.service.License import License
from storyscript.hub.sdk.service.ServiceInfo import ServiceInfo

service_info_fixture = {
    "service_info": {
        "title": "Stockbroker",
        "license": {
            "url": "https://opensource.org/licenses/MIT",
            "name": "MIT"
        },
        "version": "0.0.1",
        "description": "An http service to fetch stock prices",
        "contact": {
            "url": "https://storyscript.io",
            "name": "Aurelien ARINO",
            "email": "aurelien@storyscript.io"
        }
    }

}

service_info_fixture_json = json.dumps(service_info_fixture)


def test_deserialization(mocker):
    mocker.patch.object(json, 'loads', return_value=service_info_fixture)

    mocker.patch.object(License, 'from_dict')
    mocker.patch.object(Contact, 'from_dict')

    service_info = ServiceInfo.from_json(jsonstr=service_info_fixture_json)

    assert service_info is not None

    json.loads.assert_called_with(service_info_fixture_json)

    assert service_info.title() == service_info_fixture["service_info"]["title"]
    assert service_info.description() == service_info_fixture["service_info"]["description"]

    Contact.from_dict.assert_called_with(data={
        "contact": service_info_fixture["service_info"]["contact"]
    })

    License.from_dict.assert_called_with(data={
        "license": service_info_fixture["service_info"]["license"]
    })


def test_serialization(mocker):
    mocker.patch.object(json, 'dumps', return_value=service_info_fixture_json)

    service_event = ServiceInfo.from_dict(data=service_info_fixture)

    assert service_event.as_json(compact=True) is not None
    json.dumps.assert_called_with(service_info_fixture, sort_keys=True)

    assert service_event.as_json() is not None
    json.dumps.assert_called_with(service_info_fixture, indent=4, sort_keys=True)
