"""Repeatable route-match benchmark used to gate a future Rust accelerator."""

from __future__ import annotations

import argparse
import statistics
import time

from api_shop import ApiRegistry


def build_registry(size: int) -> ApiRegistry:
    registry = ApiRegistry()
    for index in range(size):
        path = f"/groups/{index}/users/<int:user_id>"

        def handler(ctx, data):
            return None

        registry.route(path, methods=["GET"], name=f"route_{index}")(handler)
    return registry.compile()


def benchmark(size: int, iterations: int) -> dict[str, float]:
    registry = build_registry(size)
    target = f"/groups/{size - 1}/users/42"
    samples = []
    for _ in range(7):
        started = time.perf_counter_ns()
        for _ in range(iterations):
            registry.match("GET", target)
        samples.append((time.perf_counter_ns() - started) / iterations)
    return {
        "routes": float(size),
        "median_ns": statistics.median(samples),
        "p95_sample_ns": sorted(samples)[-1],
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--iterations", type=int, default=10_000)
    args = parser.parse_args()
    for route_count in (10, 100, 1_000, 10_000):
        print(benchmark(route_count, args.iterations))
