from storyhub.sdk.service.Configuration import Configuration
from storyhub.sdk.service.ServiceObject import ServiceObject


class ServiceData(ServiceObject):
    """
    This represents an entire service stored within the Storyscript Hub.
    """

    def __init__(
        self, name, uuid, description, configuration
    ):
        super().__init__(data)

        self._name = name
        self._uuid = uuid
        self._description = description
        self._configuration = configuration

    @classmethod
    def from_dict(cls, data):
        service_data = data["service_data"]

        return cls(
            name=service_data["name"],
            uuid=service_data["uuid"],
            description=service_data["description"],
            configuration=Configuration.from_dict(
                data={"configuration": service_data["configuration"]}
            )
        )

    def name(self):
        """
        This acts as a helper for easily accessing the name of the service.
        For example the value stored within {"service":{"name":"helloworld"}}

        :return: service name
        """
        return self._name

    def uuid(self):
        return self._uuid

    def description(self):
        return self._description

    def configuration(self):
        return self._configuration
