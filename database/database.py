from pymongo import MongoClient
import ssl


class DataBase:
    def __init__(self, token):
        # Connect to db and save cursor
        self.connection = MongoClient(token, ssl_cert_reqs=ssl.CERT_NONE)
        self.database = self.connection.NYUADMoney
        self.collection = self.database.Users

    def get_subscriptions(self, status=True):
        # Get all active subscribers
        with self.connection:
            return self.collection.find({"status": status})

    def subscriber_exists(self, user_id):
        # Check if subscriber exist
        with self.connection:
            result = self.collection.find_one({"user_id": user_id})
            if result:
                return True
            return False

    def subscriber_status(self, user_id):
        # return subscriber status
        with self.connection:
            result = self.collection.find_one({"user_id": user_id})
            if result:
                return bool(result["status"])
            return False

    def add_subscriber(self, user_id, status=True):
        # Add user to subscriber list
        data = {"user_id": user_id, "status": status, "rows": 5, "image": True}
        with self.connection:
            return self.collection.insert_one(data)

    def update_subscription(self, user_id, status):
        # Update subscription status
        query = {"user_id": user_id}
        with self.connection:
            return self.collection.update_one(query, {"$set": {"status": status}})

    def update_user_data(self, user_id, login, password):
        query = {"user_id": user_id}
        data = {"login": login, "password": password}
        with self.connection:
            return self.collection.update_one(query, {"$set": data})

    def delete_user_data(self, user_id):
        query = {"user_id": user_id}
        with self.connection:
            return self.collection.update_one(query, {"$unset": {"login": 1, "password": 1}})

    def get_user_data(self, user_id):
        with self.connection:
            user = self.collection.find_one({"user_id": user_id})
            if "login" in user and "password" in user:
                return {"login": user["login"], "password": user["password"], "rows": user["rows"], "image": user["image"]}
            return None


    def update_user_settings(self, user_id, key, value):
        query = {"user_id": user_id}
        data = {key: value}
        with self.connection:
            return self.collection.update_one(query, {"$set": data})


    def close(self):
        # Close connection with db
        self.connection.close()
