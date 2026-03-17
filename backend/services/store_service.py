import json
from pathlib import Path
from datetime import datetime

# Run from backend/ directory — path is relative to that working directory
STORE_PATH = Path("data/document_store.json")

# The permanent default store — always exists, always the fallback active store
DEFAULT_STORE = "Nursing_llm_store"


# ─────────────────────────────────────────────────────────────
# Low-level persistence helpers
# ─────────────────────────────────────────────────────────────

def load_store() -> dict:
    """
    Load the full store from disk.
    Expected JSON shape:
        {
            "active_store": "store_20240317_120000",
            "stores": {
                "store_20240317_120000": [
                    {"file_id": "files/abc", "mime_type": "application/pdf"},
                    ...
                ]
            }
        }
    Legacy flat format (previous schema) is migrated automatically.
    """
    if not STORE_PATH.exists():
        print("DEBUG STORE: file not found, initialising with default store")
        default_data = {"active_store": DEFAULT_STORE, "stores": {DEFAULT_STORE: []}}
        save_store(default_data)
        return default_data

    with open(STORE_PATH, "r") as f:
        data = json.load(f)

    # ── Legacy migration ─────────────────────────────────────
    # Old schema: { "store_name": [ {file_id, mime_type}, ... ], ... }
    # Detect by absence of the "stores" key.
    if "stores" not in data:
        print("DEBUG STORE: migrating legacy flat format to new nested schema")
        migrated_stores = {}
        for key, value in data.items():
            if isinstance(value, list):
                # Normalise any plain strings to dicts
                migrated_stores[key] = [
                    v if isinstance(v, dict) else {"file_id": v, "mime_type": "application/pdf"}
                    for v in value
                ]

        # The first legacy store becomes the active store
        first_store = next(iter(migrated_stores), None)
        data = {
            "active_store": first_store,
            "stores": migrated_stores,
        }
        save_store(data)
        print(f"DEBUG STORE: migration complete — active_store={first_store}")

    # ── Guarantee default store bucket always exists ──────────
    if DEFAULT_STORE not in data["stores"]:
        print(f"DEBUG STORE: creating missing default bucket '{DEFAULT_STORE}'")
        data["stores"][DEFAULT_STORE] = []
        save_store(data)

    # ── Guarantee active_store is set and valid ───────────────
    if not data.get("active_store") or data["active_store"] not in data["stores"]:
        print(f"DEBUG STORE: active_store was missing/invalid — resetting to '{DEFAULT_STORE}'")
        data["active_store"] = DEFAULT_STORE
        save_store(data)

    return data


def save_store(data: dict):
    """Persist the document store to disk."""
    STORE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(STORE_PATH, "w") as f:
        json.dump(data, f, indent=4)


# ─────────────────────────────────────────────────────────────
# Store management
# ─────────────────────────────────────────────────────────────

def create_new_store() -> str:
    """
    Create a new timestamped store bucket and set it as the active store.
    Returns the new store name.
    """
    data = load_store()

    store_name = "store_" + datetime.now().strftime("%Y%m%d_%H%M%S")
    data["stores"][store_name] = []
    data["active_store"] = store_name

    save_store(data)
    print(f"DEBUG STORE: new store created → {store_name}")
    return store_name


def get_active_store() -> str:
    """
    Returns the name of the currently active store.
    Falls back to DEFAULT_STORE ('Nursing_llm_store') if nothing is set.
    """
    data = load_store()  # load_store() already self-heals active_store
    active = data.get("active_store", DEFAULT_STORE)
    print(f"DEBUG STORE: active_store={active}")
    return active


def set_active_store(store_name: str):
    """Manually switch the active store to a different store bucket."""
    data = load_store()

    if store_name not in data.get("stores", {}):
        raise ValueError(f"Store '{store_name}' does not exist. Create it first.")

    data["active_store"] = store_name
    save_store(data)
    print(f"DEBUG STORE: active_store switched to → {store_name}")


# ─────────────────────────────────────────────────────────────
# File management
# ─────────────────────────────────────────────────────────────

def add_file(file_id: str, mime_type: str = "application/pdf", store_name: str = None):
    """
    Append a file entry to a store bucket.
    - If store_name is provided → adds to that specific store.
    - If store_name is None    → adds to the currently ACTIVE store.
    Skips duplicates based on file_id.
    """
    data = load_store()
    target_store = store_name or data.get("active_store", DEFAULT_STORE)

    # Ensure bucket exists (edge-case safety)
    if target_store not in data["stores"]:
        print(f"DEBUG STORE: bucket '{target_store}' not found, creating it")
        data["stores"][target_store] = []

    # Check for duplicate
    existing_ids = [
        e["file_id"] if isinstance(e, dict) else e
        for e in data["stores"][target_store]
    ]

    if file_id not in existing_ids:
        data["stores"][target_store].append({"file_id": file_id, "mime_type": mime_type})
        print(f"DEBUG STORE: added '{file_id}' ({mime_type}) → store '{target_store}'")
    else:
        print(f"DEBUG STORE: '{file_id}' already in '{target_store}', skipping")

    save_store(data)


def get_active_files() -> list:
    """
    Return a list of dicts {file_id, mime_type} from the active store.
    Returns an empty list if no documents have been uploaded yet.
    """
    data = load_store()
    store_name = get_active_store()

    raw = data["stores"].get(store_name, [])

    # Normalise any legacy plain-string entries
    normalised = [
        e if isinstance(e, dict) else {"file_id": e, "mime_type": "application/pdf"}
        for e in raw
    ]

    print(f"DEBUG STORE: get_active_files() from '{store_name}' → {normalised}")
    return normalised


def get_files_from_store(store_name: str) -> list:
    """
    Return a list of dicts {file_id, mime_type} from a named store.
    Useful for querying non-active stores.
    """
    data = load_store()
    raw = data["stores"].get(store_name, [])

    normalised = [
        e if isinstance(e, dict) else {"file_id": e, "mime_type": "application/pdf"}
        for e in raw
    ]

    print(f"DEBUG STORE: get_files_from_store('{store_name}') → {normalised}")
    return normalised


def list_all_stores() -> dict:
    """Return the full store document (active_store + all store buckets)."""
    data = load_store()
    print(f"DEBUG STORE: list_all_stores() — {len(data.get('stores', {}))} store(s)")
    return data

# Alias for backward compatibility and user-defined plan steps
get_store_data = list_all_stores
