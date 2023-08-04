# (C) Datadog, Inc. 2023-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
import pytest

from datadog_checks.base import AgentCheck
from datadog_checks.dev.utils import get_metadata_metrics

from .common import HEAD_INSTANCE, METRICS, WORKER1_INSTANCE

pytestmark = [pytest.mark.e2e, pytest.mark.usefixtures("dd_environment")]


@pytest.mark.parametrize(
    'instance',
    [
        pytest.param(HEAD_INSTANCE, id='head'),
        pytest.param(WORKER1_INSTANCE, id='worker'),
    ],
)
def test_check(dd_agent_check, instance):
    aggregator = dd_agent_check(instance, rate=True)

    for expected_metric in METRICS:
        aggregator.assert_metric(f"ray.{expected_metric}")

    aggregator.assert_all_metrics_covered()
    aggregator.assert_metrics_using_metadata(get_metadata_metrics())

    aggregator.assert_service_check("ray.openmetrics.health", status=AgentCheck.OK)
