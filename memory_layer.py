import json
from config import hindsight

# We use a dedicated collection space inside Hindsight for incident management
COLLECTION_NAME = "devops_incident_hindsight"

def init_memory_store():
    """Ensures our workspace has the incident response memory collection."""
    try:
        collections = hindsight.list_collections()
        if COLLECTION_NAME not in [c.name for c in collections]:
            hindsight.create_collection(
                name=COLLECTION_NAME, 
                description="Stores telemetry snapshots, executed fixes, and incident outcomes."
            )
            print(f"📦 Created Hindsight collection: '{COLLECTION_NAME}'")
    except Exception as e:
        print(f"⚠️ Warning initializing collection: {e}. Proceeding assuming active state.")

def log_incident_outcome(incident_id: str, signature: str, action_taken: str, result: str, post_mortem: str):
    """
    Saves an entry into Hindsight so the agent can learn what worked or failed.
    """
    payload = {
        "incident_id": incident_id,
        "signature": signature,
        "action_taken": action_taken,
        "result": result, # "SUCCESS" or "FAILURE"
        "post_mortem": post_mortem
    }
    
    # Store dynamic text block for vector matching alongside raw attributes
    hindsight.insert_document(
        collection_name=COLLECTION_NAME,
        text=f"Incident Signature: {signature}\nAction attempted: {action_taken}\nOutcome status: {result}\nPost-Mortem insight: {post_mortem}",
        metadata=payload
    )

def recall_past_experiences(current_signature: str, limit: int = 3):
    """
    Queries Hindsight vector database to discover historical contexts matching this bug.
    """
    try:
        results = hindsight.search(
            collection_name=COLLECTION_NAME,
            query=current_signature,
            limit=limit
        )
        return results
    except Exception:
        # Fallback if collection is initially completely empty
        return []