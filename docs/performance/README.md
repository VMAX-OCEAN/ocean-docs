# Performance Overview

This folder documents runtime performance benchmarks, latency analysis, and
optimization strategies for the SIH-OCEAN platform.

## Files

| File | Topic |
|---|---|
| [`benchmarks.md`](benchmarks.md) | Performance benchmarks from research (Zarr vs OPeNDAP, chunk latency, etc.) |
| [`runtime-latency.md`](runtime-latency.md) | Expected runtime latency for each operation in our platform |
| [`optimization.md`](optimization.md) | Optimization strategies (chunking, caching, prefetch) |
| [`benchmark-protocol.md`](benchmark-protocol.md) | D2 runnable protocol: render latency, cold load, 30 FPS + 5000 markers, terrain bytes, ion quota, offline |
| [`chunk-benchmark-protocol.md`](chunk-benchmark-protocol.md) | D2 runnable protocol: GLORYS Zarr chunk transfer (balanced vs dual-rep), harness + pass gates |
| [`marker-format-cutoff-protocol.md`](marker-format-cutoff-protocol.md) | D2 runnable protocol: GeoJSON vs Arrow vs FlatGeobuf vs R2-JSON marker cutoff + N_LOCK rule |
| [`reference-laptop.md`](reference-laptop.md) | D2 locked reference machine (Acer A715-79G RTX 3050 144 Hz) + GPU check + browser matrix |
