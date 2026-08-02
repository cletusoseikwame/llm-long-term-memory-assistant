import uuid
import chromadb
from sentence_transformers import SentenceTransformer


class MemoryStore:
    def __init__(self, database_path="./MemoryStoreChroma_DB"):
        self.model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )

        self.client = chromadb.PersistentClient(
            path=database_path
        )

        self.memories_collection = self.client.get_or_create_collection(
            name="memories"
        )

    def add_memory(self, fact, importance):
        existing_memory = self.memories_collection.get(
            where={"fact": fact}
        )

        if existing_memory["ids"]:
            return None

        memory_id = str(uuid.uuid4())
        memory_embedding = self.model.encode(fact).tolist()

        self.memories_collection.add(
            ids=[memory_id],
            documents=[fact],
            embeddings=[memory_embedding],
            metadatas=[
                {
                    "fact": fact,
                    "importance": importance,
                }
            ],
        )

        return memory_id

    def search(self, query, k=3):
        query_embedding = self.model.encode(query).tolist()

        results = self.memories_collection.query(
            query_embeddings=[query_embedding],
            n_results=k,
            include=["documents", "metadatas", "distances"],
        )

        matched_documents = results["documents"][0]
        matched_metadatas = results["metadatas"][0]
        matched_distances = results["distances"][0]

        clean_results = []

        for document, metadata, distance in zip(
            matched_documents,
            matched_metadatas,
            matched_distances,
        ):
            clean_results.append({
                "fact": document,
                "importance": metadata["importance"],
                "distance": distance,
            })

        return clean_results


if __name__ == "__main__":
    store = MemoryStore()

    store.add_memory("I love pizza", 5)
    store.add_memory("I enjoy Italian food", 4)
    store.add_memory("I play football", 3)
    store.add_memory("I love pizza", 5)

    print(store.search("What food do I like?"))