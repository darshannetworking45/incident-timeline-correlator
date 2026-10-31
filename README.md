# Network Incident Timeline Correlator

Orders network events and groups events that occur within a configurable time window to help review a multi-device incident.

## Main entry points

- `src.correlator.NetworkEvent`
- `src.correlator.TimelineCorrelator` (`correlate`)

## Run the tests

```bash
python -m unittest discover -s tests -v
```

The project uses the Python standard library; no third-party package is required.

## Scope

Correlation is based on event timestamps and the supplied window. The tool does not infer causality or retrieve logs from devices.
