"""Module for metrics."""

import os
from collections.abc import Awaitable, Callable
from time import monotonic, perf_counter
from typing import Any

import prometheus_client
from prometheus_client import (
    CONTENT_TYPE_LATEST,
    REGISTRY,
    CollectorRegistry,
    generate_latest,
)
from prometheus_client.multiprocess import MultiProcessCollector
from starlette.requests import Request
from starlette.responses import Response

DEFAULT_BUCKETS = (
    0.005,
    0.01,
    0.025,
    0.05,
    0.075,
    0.1,
    0.125,
    0.15,
    0.175,
    0.2,
    0.25,
    0.3,
    0.5,
    0.75,
    1.0,
    2.5,
    5.0,
    7.5,
    float("+inf"),
)

REQUEST_COUNT = prometheus_client.Counter(
    "http_requests_total",
    "Total count of HTTP requests",
    ["method", "endpoint", "http_status"],
)

CLIENT_ERROR_COUNT = prometheus_client.Counter(
    "http_client_errors_total",
    "Total count of HTTP errors",
    ["method", "endpoint", "http_status"],
)

SERVER_ERROR_COUNT = prometheus_client.Counter(
    "http_server_errors_total",
    "Total count of HTTP errors",
    ["method", "endpoint", "http_status"],
)


INTEGRATIONS_LATENCY = prometheus_client.Histogram(
    "tictactoe_integrations_latency_seconds",
    "",
    ["integration"],
    buckets=DEFAULT_BUCKETS,
)

ROUTES_LATENCY = prometheus_client.Histogram(
    "tictactoe_routes_latency_seconds",
    "",
    ["method", "endpoint"],
    buckets=DEFAULT_BUCKETS,
)


def async_integrations_timer(
    func: Callable[..., Awaitable[Any]]
) -> Callable[..., Awaitable[Any]]:
    """
    Decorate to measure the execution time of asynchronous functions.

    Args:
        func (Callable[..., Awaitable[Any]]): The asynchronous function.

    Returns:
        Callable[..., Awaitable[Any]]: A wrapper function.
    """

    async def wrapper(
            *args: list[Any],
            **kwargs: dict[Any, Any]
    ) -> Awaitable[Any]:
        start_time: float = monotonic()
        result = await func(*args, **kwargs)
        INTEGRATIONS_LATENCY.labels(integration=func.__name__).observe(
            monotonic() - start_time
        )
        return result

    return wrapper


async def counter_metrics(
    request: Request, call_next: Callable[..., Awaitable[Any]]
) -> Awaitable[Any]:
    """
    Middleware function for collecting request metrics.

    Args:
        request (Request): The incoming HTTP request.
        call_next (Callable[..., Awaitable[Any]]): The next middleware.

    Returns:
        Awaitable[Any]: The response from the next middleware or route handler.
    """
    start_time = perf_counter()
    response = await call_next(request)
    process_time = perf_counter() - start_time
    if request.url.path in ("/favicon.ico", "/metrics"):
        return response
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.url.path,
        http_status=str(response.status_code),
    ).inc()
    ROUTES_LATENCY.labels(
        method=request.method,
        endpoint=request.url.path).observe(
        process_time
    )

    if 400 <= response.status_code < 500:
        CLIENT_ERROR_COUNT.labels(
            method=request.method,
            endpoint=request.url.path,
            http_status=str(response.status_code),
        ).inc()
    elif 500 <= response.status_code:
        SERVER_ERROR_COUNT.labels(
            method=request.method,
            endpoint=request.url.path,
            http_status=str(response.status_code),
        ).inc()

    return response


def metrics(request: Request) -> Response:
    """
    Endpoint for exposing Prometheus metrics.

    Args:
        request (Request): The incoming HTTP request.

    Returns:
        Response: The response containing the generated Prometheus metrics.
    """
    if "prometheus_multiproc_dir" in os.environ:
        registry = CollectorRegistry()
        MultiProcessCollector(registry)
    else:
        registry = REGISTRY

    return Response(
        generate_latest(registry),
        headers={"Content-Type": CONTENT_TYPE_LATEST}
    )
