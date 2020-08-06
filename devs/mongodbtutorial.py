import pymongo
from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://admin:adminrocks@db01.i7iwq.gcp.mongodb.net/test?retryWrites=true&w=majority")

db = cluster["test"]
collection = db["test"]

post1 = {"_id": 1, "name":"Jim", "score":8}
post2 = {"_id": 2, "name":"jone", "score":7}

# collection.insert_one(post1)

# collection.insert_many([post1, post2])

# result = collection.find({"name":"jone"})

# for r in result:
#     print(r)

# for r in result:
#     print(r["_id"])

# result = collection.find_one({"_id":2})

# print(result)

# result = collection.find({})

# for x in result:
#     print(x)

# result = collection.delete_one({"_id":0})

# result = collection.update_one({"_id":1},{"$set":{"name":"Tim"}})

# result = collection.update_one({"_id":1},{"$set":{"age":56}}) This will add a new field

# result = collection.update_one({"_id":1},{"$inc":{"age":10}}) This will 10 to age

post_count = collection.count_documents({})

print(post_count)