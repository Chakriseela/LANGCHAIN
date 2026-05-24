from pymongo import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv  
load_dotenv()  
uri = os.getenv("YOUR_MONGODB_URL")

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
    print("ERROR")

# MONGO_DB CREDENTIALS
# chakriseela111_db_user     xUnQ9obkoV5F388Z
# URL FOR MONGO_DB DOCS https://www.mongodb.com/docs/languages/python/
# URL FOR MONGODB COMPASS https://www.mongodb.com/docs/compass/
# URL FOR Python Starter Sample App https://github.com/mongodb/sample-app-python-mflix






# python -m pip install "pymongo[srv]"