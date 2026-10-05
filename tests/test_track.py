import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from race.track import Track  # noqa: E402


class TrackTest(unittest.TestCase):
    def test_empty_standings(self):
        self.assertEqual(Track(["c0"], 0).standings(), [])

    def test_single_player_time(self):
        track = Track(["c0", "c1"], 0)
        track.record("m1", "p", 0, 100)
        track.record("m2", "p", 1, 300)
        self.assertEqual(track.standings()[0][1], 200)

    def test_work_starts_at_zero(self):
        self.assertEqual(Track(["c0"], 0).work_count(), 0)


if __name__ == "__main__":
    unittest.main()
