"""Network Incident Timeline Correlator."""

from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class NetworkEvent:
    """Discrete network event with epoch timestamp."""
    timestamp_epoch: int
    source_device: str
    event_type: str
    description: str


class TimelineCorrelator:
    """Clusters operational events within a sliding temporal window."""

    @staticmethod
    def correlate(events: List[NetworkEvent], correlation_window_sec: int = 120) -> List[Dict]:
        """
        Groups events occurring within correlation_window_sec of each other.
        Identifies whether a configuration change immediately preceded an outage.
        """
        sorted_events = sorted(events, key=lambda e: e.timestamp_epoch)
        clusters: List[List[NetworkEvent]] = []

        current_cluster: List[NetworkEvent] = []
        for ev in sorted_events:
            if not current_cluster:
                current_cluster.append(ev)
            else:
                if ev.timestamp_epoch - current_cluster[0].timestamp_epoch <= correlation_window_sec:
                    current_cluster.append(ev)
                else:
                    clusters.append(current_cluster)
                    current_cluster = [ev]
        if current_cluster:
            clusters.append(current_cluster)

        reports = []
        for cluster in clusters:
            has_cfg = any(e.event_type == "CONFIG_CHANGE" for e in cluster)
            has_down = any(e.event_type in ("LINK_DOWN", "OSPF_DOWN") for e in cluster)
            probable_root_cause = (
                "Config change directly precipitated outage"
                if (has_cfg and has_down)
                else "Isolated or physical layer event"
            )

            reports.append({
                "start_time": cluster[0].timestamp_epoch,
                "duration_sec": cluster[-1].timestamp_epoch - cluster[0].timestamp_epoch,
                "event_count": len(cluster),
                "probable_root_cause": probable_root_cause,
                "events": [f"{e.source_device}: [{e.event_type}] {e.description}" for e in cluster]
            })

        return reports
