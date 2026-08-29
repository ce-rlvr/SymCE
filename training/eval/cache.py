"""Per-completion sqlite cache.

A single ``cache.sqlite`` file under ``runs/eval_cache/`` keyed by

    sha256(model_id | prompt_string | sample_idx | temperature | top_p | max_new_tokens | stop)

lets us:

- Resume a crashed eval mid-benchmark.
- Re-score completions without re-generating (cheap iteration on the answer
  extractor / oracle).
- Re-use generations across runs / suite invocations (especially valuable on
  commercial-API runs where every call costs money).

The cache is concurrency-safe for *reads* and serialises writes through the
sqlite WAL — multiple processes hitting the same DB will block briefly on
write but won't corrupt. Cache misses are not negative-cached.

The cache key intentionally **includes** ``sample_idx`` so that running
``n_samples=8`` and later running ``n_samples=4`` of the same problem reuses
the first 4 completions (instead of generating four new ones).
"""

from __future__ import annotations

import hashlib
import json
import logging
import sqlite3
import threading
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Iterable, Optional

logger = logging.getLogger(__name__)


_DDL = """
CREATE TABLE IF NOT EXISTS completions (
    cache_key       TEXT PRIMARY KEY,
    model_id        TEXT NOT NULL,
    prompt_sha      TEXT NOT NULL,
    sample_idx      INTEGER NOT NULL,
    temperature     REAL NOT NULL,
    max_new_tokens  INTEGER NOT NULL,
    completion      TEXT NOT NULL,
    stop_reason     TEXT,
    created_at      REAL NOT NULL,
    extra_json      TEXT
);
CREATE INDEX IF NOT EXISTS idx_completions_model_prompt
    ON completions(model_id, prompt_sha);
"""


def _hash(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def _normalize_stop(stop: Optional[Iterable[str]]) -> str:
    if not stop:
        return ""
    return "||".join(str(s) for s in stop)


def make_cache_key(
    model_id: str,
    prompt: str,
    sample_idx: int,
    temperature: float,
    top_p: float,
    max_new_tokens: int,
    stop: Optional[Iterable[str]] = None,
) -> str:
    """Stable cache key. ``prompt`` is the full rendered chat string (post-template)."""
    payload = "|".join(
        [
            model_id,
            _hash(prompt),
            str(int(sample_idx)),
            f"{float(temperature):.4f}",
            f"{float(top_p):.4f}",
            str(int(max_new_tokens)),
            _normalize_stop(stop),
        ]
    )
    return _hash(payload)


class CompletionCache:
    """Sqlite-backed completion cache. Use as a singleton per process."""

    def __init__(self, db_path: Path | str, enabled: bool = True):
        self.enabled = bool(enabled)
        self.db_path = Path(db_path)
        self._lock = threading.Lock()
        self._conn: Optional[sqlite3.Connection] = None
        if self.enabled:
            self.db_path.parent.mkdir(parents=True, exist_ok=True)
            self._conn = sqlite3.connect(
                str(self.db_path), check_same_thread=False, timeout=30.0
            )
            with self._lock:
                self._conn.execute("PRAGMA journal_mode=WAL")
                self._conn.execute("PRAGMA synchronous=NORMAL")
                for stmt in _DDL.split(";"):
                    if stmt.strip():
                        self._conn.execute(stmt)
                self._conn.commit()

    # ── reads ────────────────────────────────────────────────────────────────
    def get(self, cache_key: str) -> Optional[str]:
        if not self.enabled or self._conn is None:
            return None
        with self._lock:
            cur = self._conn.execute(
                "SELECT completion FROM completions WHERE cache_key = ?",
                (cache_key,),
            )
            row = cur.fetchone()
        return row[0] if row else None

    def get_many(self, cache_keys: Iterable[str]) -> dict[str, str]:
        if not self.enabled or self._conn is None:
            return {}
        keys = list(cache_keys)
        if not keys:
            return {}
        out: dict[str, str] = {}
        with self._lock:
            # Chunk to keep the parameter list under sqlite's SQLITE_MAX_VARIABLE_NUMBER
            for i in range(0, len(keys), 500):
                chunk = keys[i : i + 500]
                placeholders = ",".join("?" * len(chunk))
                cur = self._conn.execute(
                    f"SELECT cache_key, completion FROM completions "
                    f"WHERE cache_key IN ({placeholders})",
                    chunk,
                )
                for k, c in cur.fetchall():
                    out[k] = c
        return out

    # ── writes ───────────────────────────────────────────────────────────────
    def put(
        self,
        cache_key: str,
        *,
        model_id: str,
        prompt: str,
        sample_idx: int,
        temperature: float,
        max_new_tokens: int,
        completion: str,
        stop_reason: Optional[str] = None,
        extra: Optional[dict] = None,
    ) -> None:
        if not self.enabled or self._conn is None:
            return
        with self._lock:
            self._conn.execute(
                "INSERT OR REPLACE INTO completions "
                "(cache_key, model_id, prompt_sha, sample_idx, temperature, "
                " max_new_tokens, completion, stop_reason, created_at, extra_json) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    cache_key,
                    model_id,
                    _hash(prompt),
                    int(sample_idx),
                    float(temperature),
                    int(max_new_tokens),
                    completion,
                    stop_reason,
                    time.time(),
                    json.dumps(extra) if extra else None,
                ),
            )
            self._conn.commit()

    def put_many(self, rows: list[dict]) -> None:
        """rows: list of dicts with all the fields ``put`` takes."""
        if not self.enabled or self._conn is None or not rows:
            return
        now = time.time()
        with self._lock:
            self._conn.executemany(
                "INSERT OR REPLACE INTO completions "
                "(cache_key, model_id, prompt_sha, sample_idx, temperature, "
                " max_new_tokens, completion, stop_reason, created_at, extra_json) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                [
                    (
                        r["cache_key"],
                        r["model_id"],
                        _hash(r["prompt"]),
                        int(r["sample_idx"]),
                        float(r["temperature"]),
                        int(r["max_new_tokens"]),
                        r["completion"],
                        r.get("stop_reason"),
                        now,
                        json.dumps(r["extra"]) if r.get("extra") else None,
                    )
                    for r in rows
                ],
            )
            self._conn.commit()

    def stats(self) -> dict:
        if not self.enabled or self._conn is None:
            return {"enabled": False}
        with self._lock:
            cur = self._conn.execute("SELECT COUNT(*) FROM completions")
            n = cur.fetchone()[0]
            cur = self._conn.execute(
                "SELECT model_id, COUNT(*) FROM completions GROUP BY model_id"
            )
            per_model = {row[0]: row[1] for row in cur.fetchall()}
        return {"enabled": True, "n_rows": n, "per_model": per_model, "path": str(self.db_path)}

    def close(self) -> None:
        if self._conn is not None:
            with self._lock:
                self._conn.close()
            self._conn = None


_GLOBAL_CACHE: Optional[CompletionCache] = None


def get_cache(db_path: Optional[Path | str] = None, enabled: bool = True) -> CompletionCache:
    """Lazy singleton accessor. Pass db_path on first call to control location."""
    global _GLOBAL_CACHE
    if _GLOBAL_CACHE is None:
        if db_path is None:
            from training.common.paths import REPO_ROOT
            db_path = REPO_ROOT / "runs" / "eval_cache" / "cache.sqlite"
        _GLOBAL_CACHE = CompletionCache(db_path, enabled=enabled)
    return _GLOBAL_CACHE


@contextmanager
def temporary_cache(db_path: Path | str):
    """Use a non-singleton cache (handy in tests)."""
    cache = CompletionCache(db_path, enabled=True)
    try:
        yield cache
    finally:
        cache.close()
