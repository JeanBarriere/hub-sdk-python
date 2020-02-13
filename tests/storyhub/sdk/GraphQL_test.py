# -*- coding: utf-8 -*-
from storyhub.sdk.GraphQL import GraphQL


def test_get_all():
    services = GraphQL.get_all()
    assert type(services) is list  # Because the Hub has at least 10.
