
import monitor


def test_collect_metrics_returns_expected_keys():
    metrics = monitor.collect_metrics()

    assert "cpu_percent" in metrics
    assert "memory_percent" in metrics
    assert "disk_percent" in metrics


def test_check_endpoint_skips_when_url_is_empty():
    result = monitor.check_endpoint("")

    assert result == {
        "configured": False,
        "status": "skipped",
    }


def test_check_endpoint_reports_unavailable_service():
    result = monitor.check_endpoint(
        "http://127.0.0.1:1/unavailable"
    )

    assert result["configured"] is True
    assert result["status"] == "down"
