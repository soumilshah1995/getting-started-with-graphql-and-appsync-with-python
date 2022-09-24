import requests
import json
import os
from dotenv import load_dotenv
load_dotenv(".env")


class AppSync(object):
    def __init__(self,data):
        endpoint = data["endpoint"]
        self.APPSYNC_API_ENDPOINT_URL = endpoint
        self.api_key = data["api_key"]
        self.session = requests.Session()

    def graphql_operation(self,query,input_params):

        response = self.session.request(
            url=self.APPSYNC_API_ENDPOINT_URL,
            method='POST',
            headers={'x-api-key': self.api_key},
            json={'query': query,'variables':{"input":input_params}}
        )

        return response.json()



def main():
    APPSYNC_API_ENDPOINT_URL = os.getenv("APPSYNC_API_ENDPOINT_URL")
    APPSYNC_API_KEY = os.getenv("APPSYNC_API_KEY")
    init_params = {"endpoint":APPSYNC_API_ENDPOINT_URL,"api_key":APPSYNC_API_KEY}
    app_sync = AppSync(init_params)

    mutation = """
     query MyQuery {
          getUsers {
            completed
            id
            title
            userId
          }
        }

    """

    input_params = {}

    response = app_sync.graphql_operation(mutation,input_params)
    print(json.dumps(response , indent=3))

main()