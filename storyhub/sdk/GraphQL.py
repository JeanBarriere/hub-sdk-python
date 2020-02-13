# -*- coding: utf-8 -*-
import json
from os import environ
from time import sleep

import requests

api_url = environ.get(
    "STORYSCRIPT_HUB_API", "https://api.storyscript.com/graphql"
)


class GraphQL:
    @classmethod
    def get_all(cls):
        query = """
        {
            allServices {
              nodes {
                uuid
                name
                description
                configuration
              }
            }
        }
        """
        max_attempts = 5
        attempts = 0
        res = None
        while attempts < max_attempts:
            attempts += 1

            try:
                res = requests.post(
                    api_url,
                    data=json.dumps({"query": query}),
                    headers={"Content-Type": "application/json"},
                    timeout=10,
                )
                if res.status_code != 200:
                    raise Exception(
                        f"Status code is not 200, " f"but {res.status_code}!"
                    )
                break
            except BaseException as e:
                sleep(0.5)
                if attempts == max_attempts:
                    raise e

        data = res.json()
        return data["data"]["allServices"]["nodes"]
