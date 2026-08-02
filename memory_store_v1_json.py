
import json
import math

from sentence_transformers import SentenceTransformer


class MemoryStore:
    def __init__(self, file_name="memories.json"):
        self.store = []
        self.file_name = file_name
        self.model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    
    def add_memory(self, fact, importance):
        found = False
        for memory in self.store:
            if memory["fact"]== fact:
                found = True
                break

        if not found:
            memory_embedding = self.model.encode(fact)
            self.store.append({
               "fact":fact,
                "embedding": memory_embedding.tolist(),
                "importance": importance

            })
        
    
    def calculate_distance(self, vector1,vector2):
        total=0
        for index in range(len(vector1)):
            distance = (vector1[index]-vector2[index])**2
            total+=distance
        return math.sqrt(total)

    
    def search(self,query,k=3):
        query_embedding = self.model.encode(query)
        results =[]
        for memory in self.store:
            distance = self.calculate_distance(query_embedding,memory["embedding"])
            results.append({
                "fact":memory["fact"],
                "importance": memory["importance"],
                "distance": distance,
            })

        results.sort(
            key =lambda item : item["distance"] 
        )
        return results[:k]

    
    def save(self):
        with open(self.file_name, "w") as file:
            json.dump(self.store, file, indent=4)

    def load(self):
        try:
            with open(self.file_name, "r") as file:
                self.store = json.load(file)
        except FileNotFoundError:
            self.store = []


if __name__ == "__main__":
    store = MemoryStore()

    store.add_memory("I love pizza", 5)
    store.add_memory("I enjoy Italian food", 4)
    store.add_memory("I play football", 3)
    store.add_memory("I love pizza", 5)

    print(store.search("What food do I like?"))
    print("Memory count:", len(store.store))











        


