import pymongo

def add_file_to_queue(file_name):
    try:
        client = pymongo.MongoClient("mongodb://root:root@ais-mongodb:27017")
        db = client["ais"]
        collection = db["scheduled_files"]
        collection2 = db["all_files"]
        collection.insert_one({"file_name": file_name})
        collection2.insert_one({"file_name": file_name})
        return {"message": "File added to queue successfully!", "success": True}
    except Exception as e:
        return {"message": f"File addition to queue failed!{e}", "success": False}

def get_file_from_queue():
    try:
        client = pymongo.MongoClient("mongodb://root:root@ais-mongodb:27017")
        db = client["ais"]
        collection = db["scheduled_files"]
        files = []
        for x in collection.find():
            files.append(x["file_name"])
        return files
    except Exception as e:
        return {"message": f"File retrieval from queue failed!{e}", "success": False}

def remove_file_from_queue(file_name):
    try:
        client = pymongo.MongoClient("mongodb://root:root@ais-mongodb:27017")
        db = client["ais"]
        collection = db["scheduled_files"]
        collection.delete_one({"file_name": file_name})
        return {"message": "File removed from queue successfully!", "success": True}
    except Exception as e:
        return {"message": f"File removal from queue failed!{e}", "success": False}