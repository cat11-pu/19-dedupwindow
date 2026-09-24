import unittest

from dedupapi import Stream
from dedupwindow import Dedup


class TestDedup(unittest.TestCase):
    def test_first_offer_accepted(self):
        self.assertTrue(Dedup().offer("e1", 0)["accepted"])

    def test_duplicate_rejected(self):
        dedup = Dedup()
        dedup.offer("e1", 0)
        self.assertFalse(dedup.offer("e1", 1)["accepted"])

    def test_duplicate_counted(self):
        dedup = Dedup()
        dedup.offer("e1", 0)
        dedup.offer("e1", 1)
        self.assertEqual(dedup.stats()["duplicates"], 1)

    def test_stats_shape(self):
        self.assertIn("seen", Dedup().stats())

    def test_stream_wraps_dedup(self):
        stream = Stream()
        stream.offer("e1", 0)
        self.assertEqual(stream.dedup.stats()["accepted"], 1)


if __name__ == "__main__":
    unittest.main()
