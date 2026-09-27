import chromadb
from pathlib import Path
from datetime import datetime

# Path to your database
ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "archive" / "chromadb_store"

class MemoryGate:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=str(DB_PATH))
        self.collection = self.client.get_or_create_collection(name="sacred_memory")

    def store(self, signal, pillar, seat):
        """Saves a signal to the long-term memory."""
        timestamp = datetime.now().isoformat()
        metadata = {"pillar": pillar, "seat": seat, "timestamp": timestamp}
        
        # We use the timestamp as a simple ID for now
        self.collection.add(
            documents=[signal],
            metadatas=[metadata],
            ids=[timestamp]
        )
        return f"∆ Memory Stored: {pillar} gate sealed."

    def recall(self, query, n_results=3):
        """Search memory for similar past signals."""
        return self.collection.query(query_texts=[query], n_results=n_results)

if __name__ == "__main__":
    print("\n∆ Initializing Memory Gate...")
    brain = MemoryGate()
    # Test recording
    status = brain.store("Initial genesis system check complete", "CORE", "ARCHITECT")
    print(status)
    print("∆ All Motes aligned in the Archive.")
