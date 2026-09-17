"""Memory: the retrieval contract, and the gate on persistent writes."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from companyos.memory import FileMemoryStore, MemoryProposal, NullMemoryStore, RunScratchpad

from . import support


class RetrievalTest(unittest.TestCase):
    def setUp(self) -> None:
        self.store = FileMemoryStore(support.REPO_ROOT)

    def test_existing_memory_documents_are_indexed(self) -> None:
        self.assertIn("decision-memory", self.store.stores)
        self.assertIn("lessons-learned", self.store.stores)
        self.assertIn("knowledge-base", self.store.stores)

    def test_every_result_carries_the_retrieval_contract(self) -> None:
        records = self.store.retrieve("retention versioning of memory", k=3)
        self.assertTrue(records)
        for record in records:
            self.assertTrue(record.source)
            self.assertGreater(record.confidence, 0)
            self.assertGreater(record.timestamp, 0)
            self.assertGreater(record.relevance, 0)
            self.assertTrue(record.tags)

    def test_results_are_ranked_best_first(self) -> None:
        records = self.store.retrieve("context assembly for a task", k=5)
        scores = [r.relevance for r in records]
        self.assertEqual(scores, sorted(scores, reverse=True))

    def test_no_reliable_source_returns_empty(self) -> None:
        self.assertEqual(self.store.retrieve("zzzqqxx wibble frobnicator"), [])

    def test_retrieval_can_be_scoped_to_stores(self) -> None:
        records = self.store.retrieve("decision", k=5, stores=["decision-memory"])
        self.assertTrue(all(r.store == "decision-memory" for r in records))

    def test_k_is_respected(self) -> None:
        self.assertLessEqual(len(self.store.retrieve("memory", k=2)), 2)


class WriteGateTest(unittest.TestCase):
    def test_writes_are_proposals_by_default(self) -> None:
        store = FileMemoryStore(support.REPO_ROOT)
        proposal = store.propose(
            MemoryProposal(
                store="session-memory", text="A fact.", source="run:1", tags=("test",)
            )
        )
        self.assertFalse(proposal.promoted)
        self.assertEqual(len(store.proposals()), 1)

    def test_promotion_is_refused_unless_policy_allows_it(self) -> None:
        store = FileMemoryStore(support.REPO_ROOT, allow_promotion=False)
        proposal = MemoryProposal(
            store="session-memory", text="A fact.", source="run:1", tags=("test",)
        )
        result = store.promote(proposal)
        self.assertFalse(result.promoted)
        self.assertIn("disabled by runtime policy", result.rejected_reason)

    def test_unvalidated_writes_are_rejected(self) -> None:
        store = FileMemoryStore(support.REPO_ROOT, allow_promotion=True)
        for bad, reason in (
            (MemoryProposal(store="s", text="", source="run:1", tags=("t",)), "empty text"),
            (MemoryProposal(store="s", text="x", source="", tags=("t",)), "missing source"),
            (MemoryProposal(store="s", text="x", source="run:1", tags=()), "untagged"),
        ):
            with self.subTest(reason=reason):
                self.assertIn(reason, store.promote(bad).rejected_reason)

    def test_promotion_appends_to_the_right_document_when_enabled(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            memory_dir = root / "ai" / "memory"
            memory_dir.mkdir(parents=True)
            target = memory_dir / "session-memory.md"
            target.write_text("# Session Memory\n", encoding="utf-8")

            store = FileMemoryStore(root, allow_promotion=True)
            proposal = store.promote(
                MemoryProposal(
                    store="session-memory",
                    text="The chosen approach was X.",
                    source="run:1 task:2",
                    tags=("decision",),
                    agent_id="engineering/backend-engineer",
                )
            )
            self.assertTrue(proposal.promoted)
            written = target.read_text(encoding="utf-8")
            self.assertIn("The chosen approach was X.", written)
            self.assertIn("engineering/backend-engineer", written)

    def test_promotion_to_an_unknown_store_is_refused(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "ai" / "memory").mkdir(parents=True)
            store = FileMemoryStore(root, allow_promotion=True)
            result = store.promote(
                MemoryProposal(store="invented-memory", text="x", source="s", tags=("t",))
            )
            self.assertFalse(result.promoted)
            self.assertIn("unknown memory store", result.rejected_reason)


class ScratchpadTest(unittest.TestCase):
    def test_task_state_is_namespaced(self) -> None:
        scratch = RunScratchpad("run_1")
        scratch.put("draft", "alpha", task_id="t1")
        scratch.put("draft", "beta", task_id="t2")
        self.assertEqual(scratch.get("draft", task_id="t1"), "alpha")
        self.assertEqual(scratch.get("draft", task_id="t2"), "beta")

    def test_scratch_is_scoped_per_task(self) -> None:
        scratch = RunScratchpad("run_1")
        scratch.put("a", 1, task_id="t1")
        scratch.put("b", 2, task_id="t2")
        self.assertEqual(scratch.for_task("t1"), {"a": 1})

    def test_scratch_never_reaches_persistent_memory(self) -> None:
        scratch = RunScratchpad("run_1")
        scratch.put("secret", "ephemeral", task_id="t1")
        store = FileMemoryStore(support.REPO_ROOT)
        self.assertEqual(store.retrieve("ephemeral"), [])


class NullStoreTest(unittest.TestCase):
    def test_null_store_knows_nothing_but_still_records_proposals(self) -> None:
        store = NullMemoryStore()
        self.assertEqual(store.retrieve("anything"), [])
        self.assertEqual(store.stores, [])
        store.propose(MemoryProposal(store="s", text="x", source="y", tags=("t",)))
        self.assertEqual(len(store.proposals()), 1)


if __name__ == "__main__":
    unittest.main()
