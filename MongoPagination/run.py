try:
    import json

    import os
    import shutil
    import uuid
    import urllib.parse
    import pymongo
    from enum import Enum
    from bson import ObjectId

    from dotenv import load_dotenv

    load_dotenv(".env")
    print("All Modules are ok ...")
except Exception as e:
    print("Error in Imports ")


class MongoDbSettings(object):
    def __init__(self, connection_string, database_name, collection_name):
        self.connection_string = connection_string
        self.collection_name = collection_name
        self.database_name = database_name


class MongoDB:
    def __init__(self, mongo_db_settings):
        self.mongo_db_settings = mongo_db_settings

        if type(self.mongo_db_settings).__name__ != "MongoDbSettings":
            raise Exception("Please mongo_db_settings  pass correct Instance")

        self.client = pymongo.MongoClient(
            self.mongo_db_settings.connection_string,
            tls=True,
            tlsAllowInvalidCertificates=True,
        )
        self.cursor = self.client[self.mongo_db_settings.database_name][
            self.mongo_db_settings.collection_name
        ]

    def get_total_count(self, query={}, logger=None):
        total_count = self.cursor.count_documents(filter=query)

        return total_count

    def get_data_paginate(self, query={}, sort=pymongo.ASCENDING, mongo_batch_size=10):

        total_count = self.cursor.count_documents(filter=query)

        total_pages = total_count // mongo_batch_size

        page_size = mongo_batch_size

        if total_count % mongo_batch_size != 0:
            total_pages += 1
        for page_number in range(total_pages):
            skips = page_size * page_number
            data = list(
                self.cursor.find(query)
                    .skip(skips)
                    .limit(page_size)
                    .sort("createdAt", sort)
            )
            yield data

    def get_data_paginate_page_numbers(
            self, query={}, sort=pymongo.ASCENDING, mongo_batch_size=10, page_number=1
    ):

        total_count = self.cursor.count_documents(filter=query)

        total_pages = total_count // mongo_batch_size

        page_size = mongo_batch_size

        page_left_to_iterate = 0

        if page_number < total_pages:
            page_left_to_iterate = total_pages - page_number

        if total_count % mongo_batch_size != 0:
            total_pages += 1

        skips = page_size * page_number

        data = list(
            self.cursor.find(query).skip(skips).limit(page_size).sort("createdAt", sort)
        )

        return data, page_left_to_iterate


def paginate_approach_1():

    mongo_connection_string = "mongodb+srv://{}:{}@{}/?retryWrites=true&w=majority".format(
        urllib.parse.quote_plus(os.getenv("MONGO_USERNAME")),
        urllib.parse.quote_plus(os.getenv("MONGO_PASSWORD")),
        os.getenv("MONGO_DOMAIN"),
    )

    client = MongoDB(
        mongo_db_settings=MongoDbSettings(
            connection_string=mongo_connection_string,
            database_name="sample_analytics",
            collection_name="accounts",
        )
    )

    """Approach 1"""
    page = 0
    batch = 200

    response_data, page_left = client.get_data_paginate_page_numbers(
        query={}, mongo_batch_size=batch, page_number=page
    )
    print("page", page, "page_left", page_left)

    while page_left != 0:
        page = page + 1
        response_data, page_left = client.get_data_paginate_page_numbers(
            query={}, mongo_batch_size=batch, page_number=page
        )
        print("page", page, "page_left", page_left)


def paginate_approach_2():
    mongo_connection_string = "mongodb+srv://{}:{}@{}/?retryWrites=true&w=majority".format(
        urllib.parse.quote_plus(os.getenv("MONGO_USERNAME")),
        urllib.parse.quote_plus(os.getenv("MONGO_PASSWORD")),
        os.getenv("MONGO_DOMAIN"),
    )

    client = MongoDB(
        mongo_db_settings=MongoDbSettings(
            connection_string=mongo_connection_string,
            database_name="sample_analytics",
            collection_name="accounts",
        )
    )

    response_data = client.get_data_paginate(query={}, mongo_batch_size=200)
    count = 0

    while True:
        try:
            print("count", count)
            batch_data = next(response_data)
            count = count + 1
        except StopIteration:
            break
        except Exception as e:
            break
    print("total batch couunt", count)


def test():
    paginate_approach_1()
    print("-------------")
    paginate_approach_2()

test()