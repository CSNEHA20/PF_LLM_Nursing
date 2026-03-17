from fastapi import APIRouter
from services.store_service import (
    list_all_stores,
    create_new_store,
    get_active_store,
    set_active_store,
    get_files_from_store,
)

router = APIRouter()


# ── Store overview ────────────────────────────────────────────────────────────

@router.get("/stores")
def list_stores():
    """
    Returns the full store state:
    - active_store: the currently active store name
    - stores: all store buckets with their document lists
    """
    data = list_all_stores()
    return {
        "active_store": data.get("active_store"),
        "stores": data.get("stores")
    }


# ── Create new store ──────────────────────────────────────────────────────────

@router.post("/stores/new")
def create_store():
    """
    Manually create a new store and set it as active.
    All subsequent uploads will go into this store.
    """
    store_name = create_new_store()
    print(f"DEBUG: POST /stores/new → created '{store_name}'")
    return {"new_store": store_name, "message": f"Store '{store_name}' created and set as active."}


# ── Switch active store ───────────────────────────────────────────────────────

@router.post("/stores/activate/{store_name}")
def activate_store(store_name: str):
    """
    Switch the active store to an existing store by name.
    Uploads after this call will go into the selected store.
    """
    try:
        set_active_store(store_name)
        print(f"DEBUG: POST /stores/activate → switched to '{store_name}'")
        return {"active_store": store_name, "message": f"Active store switched to '{store_name}'."}
    except ValueError as e:
        return {"error": str(e)}


# ── Per-store document list (backward compat) ─────────────────────────────────

@router.get("/documents/{store_name}")
def list_documents_by_store(store_name: str):
    """
    Returns all documents in the named store bucket.
    Example: GET /api/documents/store_20240317_120000
    """
    try:
        files = get_files_from_store(store_name)
        print(f"DEBUG: GET /documents/{store_name} → {len(files)} file(s)")
        return {
            "store": store_name,
            "documents": files,
            "count": len(files),
        }
    except Exception as e:
        print(f"DEBUG ERROR in /documents/{store_name}:", str(e))
        return {"error": str(e)}


# ── Active store documents (convenience) ─────────────────────────────────────

@router.get("/documents")
def list_active_documents():
    """
    Returns documents in the currently active store.
    Convenience alias for GET /api/documents/{active_store_name}.
    """
    try:
        data = list_all_stores()
        active = data.get("active_store")

        if not active:
            return {"active_store": None, "documents": [], "count": 0}

        files = get_files_from_store(active)
        print(f"DEBUG: GET /documents (active='{active}') → {len(files)} file(s)")
        return {
            "active_store": active,
            "documents": files,
            "count": len(files),
        }
    except Exception as e:
        print("DEBUG ERROR in GET /documents:", str(e))
        return {"error": str(e)}
