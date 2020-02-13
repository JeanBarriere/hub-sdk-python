import json
from uuid import UUID

from cachetools import TTLCache, cached

from storyhub.sdk.GraphQL import GraphQL
from storyhub.sdk.service.ServiceData import ServiceData


class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            return obj.hex
        return json.JSONEncoder.default(self, obj)


class ServiceWrapper:
    """
    The ServiceWrapper provides an improved way to access storyscript
    hub services.
    """

    ttl_cache_for_all_services = TTLCache(maxsize=1, ttl=1 * 60)

    def __init__(self, services=None):
        self.services = {}
        self.reload_services(services)

    @classmethod
    def from_dict(cls, dictionary=None):
        services = []

        if dictionary is not None:
            services = dictionary

        return cls(services)

    @classmethod
    def from_json(cls, jsonstr):
        services = []

        if jsonstr is not None:
            services = json.loads(jsonstr)

        return cls(services)

    @classmethod
    def from_json_file(cls, path):
        with open(path, "r") as f:
            jsonstr = f.read()
            return cls.from_json(jsonstr=jsonstr)

    @cached(cache=ttl_cache_for_all_services)
    def fetch_services(self):
        # At the moment we are fetching all services in this function.
        # This is acceptable at the moment since entire hub data is small
        # for the time being but we will add more specialized GraphQl request
        # here later on.
        raw_services = GraphQL.get_all()
        services = {}
        for service in raw_services:
            services[service["service"]["name"]] = service
        return services

    def get_services(self, services):
        """
        Given a list of service names, returns a list of services that
        were found on the hub along with their data in a dict.

        Params:
            services (List[str]): list of service names to get data for.

        Returns:
            List[Dict[str, Any]]: list of services found with the data in dict.
        """
        services_map = self.fetch_services()

        return [
            services_map[service]
            for service in services
            if service in services_map
        ]

    def update_service(self, service, services_dict):
        """
        Puts a given service dict into services map.

        Params:
            service (Dict[str, Any]): map of service related data from hub.
            services_dict (Dict[str, Dict[str, Any]]): map of service names
                to service data.
        """
        services_dict[service["service"]["name"]] = service

    def reload_services(self, services):
        if services is None:
            return

        if all(isinstance(service, str) for service in services):
            services = self.get_services(services)
        assert all(isinstance(service, dict) for service in services)

        services_dict = {}
        for service in services:
            self.update_service(service, services_dict)

        # reset services
        self.services = services_dict

    def as_json(self):
        services = []

        for service in self.services:
            services.append(self.services[service])

        return json.dumps(services, indent=4, sort_keys=True, cls=UUIDEncoder)

    def as_json_file(self, out_file):
        if out_file is not None:
            with open(out_file, "w") as f:
                f.write(self.as_json())

    def get_all_service_names(self):
        service_names = []

        for service in self.services:
            service_names.append(service)
        return service_names

    def get(self, name=None):
        service = None

        if name in self.services:
            service = self.services[name]

        if service is None:
            return None
        else:
            return ServiceData.from_dict(data={"service_data": service})
