import pytest
from datetime import datetime

# Import the analytics module once it exists
# Tests follow RED-GREEN-REFACTOR TDD cycle

class TestPostMetricsModel:
    """Analytics metric model tests."""

    def test_create_post_metrics_with_all_fields(self):
        from postspoke.analytics import PostMetrics
        m = PostMetrics(
            post_id="p1",
            scheduled_time=datetime(2026, 9, 10, 10, 0, 0),
            reach=1000,
            clicks=50,
            conversions=5,
        )
        assert m.post_id == "p1"
        assert m.reach == 1000
        assert m.clicks == 50
        assert m.conversions == 5
        assert m.ctr == 5.0  # clicks/reach * 100
        assert m.conversion_rate == 10.0  # conversions/clicks * 100

    def test_create_post_metrics_reaches_zero(self):
        from postspoke.analytics import PostMetrics
        m = PostMetrics(
            post_id="p2",
            scheduled_time=datetime(2026, 9, 10, 11, 0, 0),
            reach=0,
            clicks=0,
            conversions=0,
        )
        assert m.ctr == 0.0
        assert m.conversion_rate == 0.0

    def test_negative_reach_raises(self):
        from postspoke.analytics import PostMetrics
        with pytest.raises(ValueError):
            PostMetrics("p3", datetime.now(), reach=-1, clicks=0, conversions=0)

class TestAggregateMetrics:
    """Aggregation logic tests."""

    def test_aggregate_single_post(self):
        from postspoke.analytics import PostMetrics, aggregate_metrics
        m = PostMetrics("p1", datetime.now(), reach=100, clicks=10, conversions=2)
        result = aggregate_metrics([m])
        assert result["total_reach"] == 100
        assert result["total_clicks"] == 10
        assert result["total_conversions"] == 2
        assert result["avg_ctr"] == 10.0
        assert result["avg_conversion_rate"] == 20.0

    def test_aggregate_empty_list(self):
        from postspoke.analytics import aggregate_metrics
        result = aggregate_metrics([])
        assert result["total_reach"] == 0
        assert result["total_clicks"] == 0
        assert result["total_conversions"] == 0

    def test_aggregate_multiple_posts(self):
        from postspoke.analytics import PostMetrics, aggregate_metrics
        posts = [
            PostMetrics("p1", datetime.now(), reach=200, clicks=20, conversions=4),
            PostMetrics("p2", datetime.now(), reach=300, clicks=30, conversions=6),
        ]
        result = aggregate_metrics(posts)
        assert result["total_reach"] == 500
        assert result["total_clicks"] == 50
        assert result["total_conversions"] == 10
        assert result["post_count"] == 2

class TestReportGenerator:
    """JSON report and CLI table tests."""

    def test_generate_json_report(self, tmp_path):
        from postspoke.analytics import PostMetrics, generate_json_report
        m = PostMetrics("p1", datetime(2026, 9, 10, 10, 0, 0), reach=100, clicks=10, conversions=2)
        path = tmp_path / "report.json"
        generate_json_report([m], str(path))
        import json
        data = json.loads(path.read_text())
        assert data["total_reach"] == 100
        assert data["posts"][0]["post_id"] == "p1"

    def test_generate_cli_summary(self, capsys):
        from postspoke.analytics import PostMetrics, generate_cli_summary
        m = PostMetrics("p1", datetime(2026, 9, 10, 10, 0, 0), reach=1000, clicks=50, conversions=5)
        generate_cli_summary([m])
        captured = capsys.readouterr()
        assert "1000" in captured.out
        assert "50" in captured.out
        assert "5.0%" in captured.out
