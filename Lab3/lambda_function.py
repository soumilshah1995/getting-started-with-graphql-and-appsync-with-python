try:
    import json

    import os
    import shutil
    import uuid
    import urllib.parse
    import pymongo
    from bson import ObjectId

    from dotenv import load_dotenv
    load_dotenv(".env")
    print("All Modules are ok ...")
except Exception as e:
    print("Error in Imports ")


def mongo_client():
    try:

        username = urllib.parse.quote_plus(os.getenv("MONGO_USERNAME"))
        password = urllib.parse.quote_plus(os.getenv("MONGO_PASSWORD"))
        mongo_connection_string = "mongodb+srv://{}:{}@{}/?retryWrites=true&w=majority".format(
            username, password, os.getenv("MONGO_DOMAIN")
        )
        client_mongo__ = pymongo.MongoClient(mongo_connection_string,
                                             tls=True,
                                             tlsAllowInvalidCertificates=True

                                             )
        return client_mongo__

    except Exception as e:
        print("erroe", e)
        return None


def handler(event=None, context=None):
    if event.get("info").get("fieldName") == "getAccountId":
        """
        Add business Logic here 
        """

        feilds = event.get("arguments")
        id  =  feilds.get("id")
        print("id", id)


        client = mongo_client()
        print("client" , client)

        resposne = client['sample_analytics']['accounts'].find_one(
            {"_id":ObjectId(id)}
        )
        resposne["_id"] = resposne["_id"].__str__()
        print("resposne", resposne)
        return resposne


# def test():
#     client = mongo_client()
#     resposne = client['sample_analytics']['accounts'].find_one(
#         {"_id":ObjectId("5ca4bbc7a2dd94ee5816238c")}
#     )
#     resposne["_id"] = resposne["_id"].__str__()
#
#     print(resposne)
#     return json.dumps(resposne)
#
#
# test()