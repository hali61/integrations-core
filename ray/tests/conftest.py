# (C) Datadog, Inc. 2023-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
import copy
import os
import time
from urllib.parse import urljoin

import pytest
import requests

from datadog_checks.dev import docker_run
from datadog_checks.dev.conditions import CheckEndpoints, WaitFor
from datadog_checks.dev.http import MockResponse
from datadog_checks.ray import RayCheck

from .common import (
    E2E_METADATA,
    HEAD_DASHBOARD_PORT,
    HEAD_INSTANCE,
    HEAD_METRICS_PORT,
    HEAD_OPENMETRICS_ENDPOINT,
    HERE,
    MOCKED_HEAD_INSTANCE,
    MOCKED_WORKER_INSTANCE,
    RAY_VERSION,
    SERVE_PORT,
    SERVE_URL,
    WORKER1_INSTANCE,
    WORKER1_METRICS_PORT,
    WORKER1_OPENMETRICS_ENDPOINT,
    WORKER2_INSTANCE,
    WORKER2_METRICS_PORT,
    WORKER2_OPENMETRICS_ENDPOINT,
    WORKER3_INSTANCE,
    WORKER3_METRICS_PORT,
    WORKER3_OPENMETRICS_ENDPOINT,
)


@pytest.fixture(scope='session')
def dd_environment():

    with docker_run(
        compose_file=os.path.join(
            HERE,
            "docker",
            "docker-compose.yaml",
        ),
        env_vars={
            "RAY_VERSION": RAY_VERSION,
            "HEAD_METRICS_PORT": HEAD_METRICS_PORT,
            "HEAD_DASHBOARD_PORT": HEAD_DASHBOARD_PORT,
            "WORKER1_METRICS_PORT": WORKER1_METRICS_PORT,
            "WORKER2_METRICS_PORT": WORKER2_METRICS_PORT,
            "WORKER3_METRICS_PORT": WORKER3_METRICS_PORT,
            "SERVE_PORT": SERVE_PORT,
        },
        conditions=[
            CheckEndpoints(HEAD_OPENMETRICS_ENDPOINT),
            CheckEndpoints(WORKER1_OPENMETRICS_ENDPOINT),
            CheckEndpoints(WORKER2_OPENMETRICS_ENDPOINT),
            CheckEndpoints(WORKER3_OPENMETRICS_ENDPOINT),
            CheckEndpoints(urljoin(SERVE_URL, "hello")),
            WaitFor(run_add),
        ],
    ):
        # Exercise the service a bit
        for _ in range(10):
            run_add()
            time.sleep(1)

        yield {
            "init_config": {},
            "instances": [
                HEAD_INSTANCE,
                WORKER1_INSTANCE,
                WORKER2_INSTANCE,
                WORKER3_INSTANCE,
            ],
        }, E2E_METADATA


@pytest.fixture
def check():
    return lambda instance: RayCheck('ray', {}, [instance])


@pytest.fixture
def head_instance():
    return copy.deepcopy(HEAD_INSTANCE)


@pytest.fixture
def worker_instance():
    return copy.deepcopy(WORKER1_INSTANCE)


@pytest.fixture
def mocked_head_instance():
    return copy.deepcopy(MOCKED_HEAD_INSTANCE)


@pytest.fixture
def mocked_worker_instance():
    return copy.deepcopy(MOCKED_WORKER_INSTANCE)


def run_add():
    try:
        response = requests.post(
            urljoin(SERVE_URL, "add"),
            data='{"a": 1, "b": 2}',
            headers={'Content-Type': 'application/json'},
        )
        response.raise_for_status()
    except Exception:
        return False
    else:
        return response.status_code == 200


def mock_http_responses(url, **_params):
    mapping = {
        'http://ray-head:8080': 'ray_head.txt',
        'http://ray-worker:8081': 'ray_worker.txt',
    }

    metrics_file = mapping.get(url)

    if not metrics_file:
        raise Exception(f"url `{url}` not registered")

    with open(os.path.join(HERE, 'fixtures', metrics_file)) as f:
        return MockResponse(content=f.read())
