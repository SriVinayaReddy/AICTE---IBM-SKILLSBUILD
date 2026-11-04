"""
In-memory data store with optional IBM Cloudant persistence.
Falls back to a local dict store when Cloudant is not configured.
"""
import uuid
import logging
from datetime import datetime
from typing import Any, Optional
from config import config

logger = logging.getLogger(__name__)

# ─── In-memory store (always available) ────────────────────────────────────
_store: dict[str, dict] = {}


def _now() -> str:
    return datetime.utcnow().isoformat() + "Z"


# ─── Cloudant helpers ───────────────────────────────────────────────────────
def _get_cloudant():
    """Return a live Cloudant client or None."""
    if not config.CLOUDANT_URL or not config.CLOUDANT_API_KEY:
        return None
    try:
        from ibmcloudant.cloudant_v1 import CloudantV1
        from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

        auth = IAMAuthenticator(config.CLOUDANT_API_KEY)
        client = CloudantV1(authenticator=auth)
        client.set_service_url(config.CLOUDANT_URL)
        return client
    except Exception as exc:
        logger.warning("Cloudant unavailable: %s", exc)
        return None


# ─── Public CRUD ────────────────────────────────────────────────────────────
def save_document(collection: str, doc: dict, doc_id: Optional[str] = None) -> str:
    """Save a document and return its ID."""
    doc_id = doc_id or str(uuid.uuid4())
    doc = {**doc, "_id": doc_id, "collection": collection, "updated_at": _now()}

    # Try Cloudant
    cloudant = _get_cloudant()
    if cloudant:
        try:
            cloudant.put_document(
                db=config.CLOUDANT_DB_NAME,
                doc_id=doc_id,
                document=doc,
            ).get_result()
            logger.debug("Saved to Cloudant: %s/%s", collection, doc_id)
        except Exception as exc:
            logger.warning("Cloudant save failed, falling back to memory: %s", exc)

    # Always mirror in memory
    _store[f"{collection}/{doc_id}"] = doc
    return doc_id


def get_document(collection: str, doc_id: str) -> Optional[dict]:
    """Retrieve a document by collection and ID."""
    # Try Cloudant first
    cloudant = _get_cloudant()
    if cloudant:
        try:
            result = cloudant.get_document(
                db=config.CLOUDANT_DB_NAME,
                doc_id=doc_id,
            ).get_result()
            if result.get("collection") == collection:
                return result
        except Exception:
            pass

    return _store.get(f"{collection}/{doc_id}")


def update_document(collection: str, doc_id: str, updates: dict) -> bool:
    """Patch an existing document."""
    existing = get_document(collection, doc_id)
    if not existing:
        return False
    merged = {**existing, **updates, "updated_at": _now()}
    save_document(collection, merged, doc_id)
    return True


def list_documents(collection: str) -> list[dict]:
    """List all documents in a collection (memory only for listing)."""
    prefix = f"{collection}/"
    return [v for k, v in _store.items() if k.startswith(prefix)]


def delete_document(collection: str, doc_id: str) -> bool:
    key = f"{collection}/{doc_id}"
    if key in _store:
        del _store[key]
        return True
    return False
