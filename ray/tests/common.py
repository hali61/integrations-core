# (C) Datadog, Inc. 2023-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)

import os

from datadog_checks.dev import get_docker_hostname, get_here

HERE = get_here()

RAY_VERSION = os.environ.get("RAY_VERSION")

SERVE_PORT = "8000"
HEAD_METRICS_PORT = "8080"
WORKER1_METRICS_PORT = "8081"
WORKER2_METRICS_PORT = "8082"
WORKER3_METRICS_PORT = "8083"
HEAD_DASHBOARD_PORT = "8265"

HEAD_OPENMETRICS_ENDPOINT = f"http://{get_docker_hostname()}:{HEAD_METRICS_PORT}"
WORKER1_OPENMETRICS_ENDPOINT = f"http://{get_docker_hostname()}:{WORKER1_METRICS_PORT}"
WORKER2_OPENMETRICS_ENDPOINT = f"http://{get_docker_hostname()}:{WORKER2_METRICS_PORT}"
WORKER3_OPENMETRICS_ENDPOINT = f"http://{get_docker_hostname()}:{WORKER3_METRICS_PORT}"
SERVE_URL = f"http://{get_docker_hostname()}:{SERVE_PORT}"
