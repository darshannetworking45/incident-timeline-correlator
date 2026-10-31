import unittest
from src.correlator import NetworkEvent, TimelineCorrelator

class TestCorrelator(unittest.TestCase):
    def test_correlation(self):
        events = [
            NetworkEvent(100, "core-01", "CONFIG_CHANGE", "Engineer applied no router ospf 1"),
            NetworkEvent(110, "core-01", "OSPF_DOWN", "Neighbor 10.0.0.2 went down"),
            NetworkEvent(115, "dist-01", "LINK_DOWN", "Gi0/1 line protocol down"),
            NetworkEvent(500, "access-01", "LINK_DOWN", "Port disconnected by user")
        ]
        clusters = TimelineCorrelator.correlate(events, correlation_window_sec=60)
        self.assertEqual(len(clusters), 2)
        self.assertIn("Config change", clusters[0]["probable_root_cause"])
        self.assertEqual(clusters[0]["event_count"], 3)
        self.assertEqual(clusters[1]["event_count"], 1)

if __name__ == "__main__":
    unittest.main()
