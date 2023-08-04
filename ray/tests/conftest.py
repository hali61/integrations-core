# (C) Datadog, Inc. 2023-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
import os
import time
from urllib.parse import urljoin

import pytest
import requests

from datadog_checks.dev import docker_run
from datadog_checks.dev.conditions import CheckEndpoints, WaitFor

from .common import (
    E2E_METADATA,
    HEAD_DASHBOARD_PORT,
    HEAD_METRICS_PORT,
    HEAD_OPENMETRICS_ENDPOINT,
    HEAD_OPENMETRICS_INSTANCE,
    HERE,
    RAY_VERSION,
    SERVE_PORT,
    SERVE_URL,
    WORKER1_METRICS_PORT,
    WORKER1_OPENMETRICS_ENDPOINT,
    WORKER1_OPENMETRICS_INSTANCE,
    WORKER2_METRICS_PORT,
    WORKER2_OPENMETRICS_ENDPOINT,
    WORKER2_OPENMETRICS_INSTANCE,
    WORKER3_METRICS_PORT,
    WORKER3_OPENMETRICS_ENDPOINT,
    WORKER3_OPENMETRICS_INSTANCE,
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
            "init_config": {
                "service": "ray-service",
            },
            "instances": [
                HEAD_OPENMETRICS_INSTANCE,
                WORKER1_OPENMETRICS_INSTANCE,
                WORKER2_OPENMETRICS_INSTANCE,
                WORKER3_OPENMETRICS_INSTANCE,
            ],
        }, E2E_METADATA


@pytest.fixture
def instance():
    return {}


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
