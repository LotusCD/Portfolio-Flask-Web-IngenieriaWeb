from pymongo import MongoClient

'''
Sin usar. En caso de requerir base de datos propia
'''

def manage_database(mongo):
    # Check if the "peliculas" database exists
    
    # print("MONGO: ", mongo.db.list_collection_names, dir(mongo.db.list_collection_names))
    # database_name = mongo.db.name
    # print(database_name) 

    db = mongo.db

    # Check if the "iudigital_db" exists in the database
    collection_names = db.list_collection_names()
    
    if 'iudigital_db' not in collection_names:
        # If "iudigital_db" doesn't exist, create it and insert a dummy document
        iudigital_db = db.iudigital_db
        iudigital_db.insert_one({"dummy": "data"})
        print("Database and collection created with dummy data.")
    else:
        # If "iudigital_db" exists, just insert some data
        iudigital_db = db.iudigital_db
        iudigital_db.insert_one({"data": "new_data"})
        print("Data added to existing collection.")

    return db_names
