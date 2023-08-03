# (C) Datadog, Inc. 2023-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
import os

import pytest

from datadog_checks.dev import docker_run
from datadog_checks.dev.conditions import CheckEndpoints

from .common import (
    HEAD_DASHBOARD_PORT,
    HEAD_METRICS_PORT,
    HEAD_OPENMETRICS_ENDPOINT,
    HERE,
    RAY_VERSION,
    WORKER1_METRICS_PORT,
    WORKER1_OPENMETRICS_ENDPOINT,
    WORKER2_METRICS_PORT,
    WORKER2_OPENMETRICS_ENDPOINT,
    WORKER3_METRICS_PORT,
    WORKER3_OPENMETRICS_ENDPOINT,
)


@pytest.fixture(scope='session')
def dd_environment():

    with docker_run(
        build=True,
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
        },
        conditions=[
            CheckEndpoints(HEAD_OPENMETRICS_ENDPOINT),
            CheckEndpoints(WORKER1_OPENMETRICS_ENDPOINT),
            CheckEndpoints(WORKER2_OPENMETRICS_ENDPOINT),
            CheckEndpoints(WORKER3_OPENMETRICS_ENDPOINT),
        ],
        sleep=10,
    ):
        yield {}


@pytest.fixture
def instance():
    return {}
