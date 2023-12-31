# Created by Egehan Kılıçarslan on 30/12/2023
# This file is part of a project developed by Egehan Kılıçarslan.

from ast import literal_eval
from dotenv import load_dotenv
from os import getenv
from secrets import token_hex
from pymongo import MongoClient
from typing import Any, Dict, Optional


class Config:
    """
    A class that represents the configuration settings for the bot.

    Attributes:
        vars (dict): A dictionary containing the configuration variables.

    Methods:
        __init__(): Initializes the Config object and loads variables from the .env file.
        __getattr__(key: str): Retrieves the value of a configuration variable.

    """

    def __init__(self) -> None:
        load_dotenv()  # Load variables from the .env file
        self.vars = {
            "TOKEN": getenv("TOKEN", ""),
            "DATABASE_URL": getenv("DATABASE_URL", ""),
            "DATABASE_CLUSTER": getenv("DATABASE_CLUSTER", ""),
            "DATABASE_USERS": getenv("DATABASE_USERS", ""),
            "DATABASE_SERVERS": getenv("DATABASE_SERVERS", ""),
            "OWNER": literal_eval(getenv("OWNER", "[]")),
            "STAFF": literal_eval(getenv("STAFF", "[]")),
            "VIP": literal_eval(getenv("VIP", "[]")),
            "SUCCESS_COLOR": getenv("SUCCESS_COLOR", ""),
            "ERROR_COLOR": getenv("ERROR_COLOR", ""),
            "SERVERS": literal_eval(getenv("SERVERS", "[]")),
        }

    def __getattr__(self, key: str):
        return self.vars.get(key, [])


class MongoDBManager:
    """
    A class that represents a MongoDB manager.

    Attributes:
        client (Any): The MongoDB client.
        db (Any): The MongoDB database.

    Methods:
        __init__(database_url: str, database_name: str): Initializes the MongoDBManager object and connects to the database.
        insert_document(collection: Any, document: Dict[str, Any]): Inserts a document into a collection.
        find_document(collection: Any, query: Dict[str, Any], projection: Optional[Dict[str, Any]] = None): Finds a document in a collection.
    """

    def __init__(self, database_url: str = Config().DATABASE_URL, database_name: str = Config().DATABASE_CLUSTER) -> None:
        self.client: Any = MongoClient(database_url)
        self.db: Any = self.client[database_name]

    def insert_document(self, collection: Any, document: Dict[str, Any]) -> Any:
        collection_name = {
            Config().DATABASE_USERS: self.db[Config().DATABASE_USERS],
            Config().DATABASE_SERVERS: self.db[Config().DATABASE_SERVERS],
        }.get(collection, collection)

        return collection_name.insert_one(document).inserted_id

    def find_document(self, collection: Any, query: Dict[str, Any], projection: Optional[Dict[str, Any]] = None) -> Any:
        collection_name = {
            Config().DATABASE_USERS: self.db[Config().DATABASE_USERS],
            Config().DATABASE_SERVERS: self.db[Config().DATABASE_SERVERS],
        }.get(collection, collection)

        return collection_name.find_one(query, projection)


def generate_secret() -> str:
    """Generate a random password of specified length"""
    return token_hex(10)
