import os
import requests

from infra_helpers.logs import PrintError
from infra_helpers.state import GetResourceValue


def Apply(resource):
    jsonResponse = None
    id = resource["id"]

    try:
        if resource["type"] == "droplet":
            response = requests.post(
                "https://api.digitalocean.com/v2/droplets",
                json={
                    "name": id,
                    "region": GetResourceValue(resource, "region", ""),
                    "size": GetResourceValue(resource, "size", ""),
                    "image": GetResourceValue(resource, "image", ""),
                    "ssh_keys": GetResourceValue(resource, "ssh_keys", []),
                    "backups": GetResourceValue(resource, "backups", False),
                    "ipv6": GetResourceValue(resource, "ipv6", False),
                    "monitoring": GetResourceValue(resource, "monitoring", True),
                    "user_data": GetResourceValue(resource, "user_data", ""),
                    "tags": GetResourceValue(resource, "tags", []),
                },
                headers={
                    "Authorization": "Bearer {}".format(os.getenv("DIGITALOCEAN_TOKEN"))
                },
            )
            jsonResponse = response.json()

    except Exception as e:
        PrintError(e)
        PrintError("Failed to create digitalocean resource with id {}".format(id))
        exit(1)

    return {
        "jsonResponse": jsonResponse,
        "dropletId": jsonResponse["droplet"]["id"],
    }


def Destroy(resource, state):
    id = resource["id"]

    try:
        if resource["type"] == "droplet":
            createJsonResponse = state["jsonResponse"]
            idOfCreatedDroplet = createJsonResponse["droplet"]["id"]
            response = requests.delete(
                "https://api.digitalocean.com/v2/droplets/{}".format(
                    idOfCreatedDroplet
                ),
                headers={
                    "Authorization": "Bearer {}".format(os.getenv("DIGITALOCEAN_TOKEN"))
                },
            )

            if response.status_code != 204:
                PrintError(response.json())
                PrintError(
                    "Failed to destroy digitalocean resource with id {}".format(id)
                )
                exit(1)

    except Exception as e:
        PrintError(e)
        PrintError("Failed to destroy digitalocean resource with id {}".format(id))
        exit(1)

    return None
