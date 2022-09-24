try:
    import json

    import os
    import shutil
    import uuid
    print("All Modules are ok ...")
except Exception as e:
    print("Error in Imports ")


def getUsers(event, context):

    if event.get("info").get("fieldName") == "getUsers":
        """
        Add business Logic here 
        """
        return {
                "userId": 1,
                "id": 1,
                "title": "delectus aut autem",
                "completed": False
            }


