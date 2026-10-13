"""Minimal offline repair for the advanced-B teaching sample."""
import copy
import hashlib
import json
import time
import uuid


class Engine:
    def __init__(self):
        self.cache = {}

    @staticmethod
    def _scope(request, corpus):
        return [
            block for block in corpus
            if block.get("doc_id") in request.get("doc_ids", [])
            and block.get("snapshot") == request.get("snapshot")
        ]

    @staticmethod
    def _cache_key(request, corpus, draft):
        payload = {
            "request": request,
            "corpus": corpus,
            "draft": draft,
        }
        raw = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    def evaluate(self, request, corpus, draft):
        started = time.perf_counter()
        scope = self._scope(request, corpus)
        request_id = str(uuid.uuid4())
        key = self._cache_key(request, corpus, draft)
        cache_hit = key in self.cache

        if cache_hit:
            result = copy.deepcopy(self.cache[key])
        else:
            terms = set(request.get("query", "").strip().lower().split())
            if not scope:
                result = {
                    "status": "invalid_scope",
                    "answer": draft.get("answer"),
                    "citations": copy.deepcopy(draft.get("citations", [])),
                    "evidence": [],
                    "locator_status": "invalid" if draft.get("citations") else "absent",
                    "support_status": "not_checked",
                    "judgment_source": "rule",
                }
            else:
                ranked = sorted(
                    scope,
                    key=lambda block: (-len(terms.intersection(set(block.get("tags", [])))), block["id"]),
                )
                evidence = [
                    block for block in ranked
                    if terms.intersection(set(block.get("tags", [])))
                ][: max(0, int(request.get("k", 0)))]
                citations = copy.deepcopy(draft.get("citations", []))
                evidence_ids = {block["id"] for block in evidence}
                if not citations:
                    locator_status = "absent"
                elif set(citations).issubset(evidence_ids):
                    locator_status = "valid"
                else:
                    locator_status = "invalid"
                result = {
                    "status": "ok",
                    "answer": draft.get("answer"),
                    "citations": citations,
                    "evidence": copy.deepcopy(evidence),
                    "locator_status": locator_status,
                    "support_status": "not_checked",
                    "judgment_source": "rule",
                }
            self.cache[key] = copy.deepcopy(result)

        result.update(
            request_id=request_id,
            request=copy.deepcopy(request),
            actual_scope={
                "doc_ids": copy.deepcopy(request.get("doc_ids", [])),
                "snapshot": request.get("snapshot"),
            },
            cache_hit=cache_hit,
            elapsed_ms=(time.perf_counter() - started) * 1000,
            run_kind="offline_replay",
        )
        return result
