from src.database import InMemoryDatabase


class History:
    def __init__(self):
        self.db = InMemoryDatabase()
        self.collection = self.db.get_collection("history")

    def insert_one(self, document):
        self.collection.insert_one(document)

    def get_history(self):
        history = [x for x in self.collection.find({}, {"_id": 0})]
        return history
