import unittest
from uuid import UUID
from src.ticket_state import can_transition
from src.rank_fusion import rrf_fuse


class TicketStateTests(unittest.TestCase):
    # These five scenarios are adapted from the original project's tests.
    def test_happy_path(self):
        for a, b in [('open','assigned'), ('assigned','in_progress'),
                     ('in_progress','resolved'), ('resolved','closed')]:
            self.assertTrue(can_transition(a, b))

    def test_direct_close(self):
        self.assertTrue(can_transition('open', 'closed'))

    def test_escalation(self):
        self.assertTrue(can_transition('in_progress', 'escalated'))
        self.assertTrue(can_transition('escalated', 'in_progress'))

    def test_closed_is_terminal(self):
        self.assertFalse(can_transition('closed', 'open'))
        self.assertFalse(can_transition('closed', 'resolved'))
        self.assertTrue(can_transition('closed', 'closed'))

    def test_cannot_reopen_resolved(self):
        self.assertFalse(can_transition('resolved', 'open'))
        self.assertFalse(can_transition('resolved', 'in_progress'))


class RankFusionTests(unittest.TestCase):
    # Added by Codex for this isolated review, using synthetic identifiers only.
    def test_shared_evidence_accumulates_across_rankings(self):
        a, b, c = UUID(int=1), UUID(int=2), UUID(int=3)
        scores = rrf_fuse([a, b], [c, a])
        self.assertAlmostEqual(scores[a], 1/61 + 1/62)
        self.assertGreater(scores[a], scores[b])
        self.assertGreater(scores[a], scores[c])

    def test_empty_rankings(self):
        self.assertEqual(rrf_fuse([], []), {})

    def test_rank_weight(self):
        a, b = UUID(int=1), UUID(int=2)
        scores = rrf_fuse([a, b])
        self.assertGreater(scores[a], scores[b])


if __name__ == '__main__':
    unittest.main()
