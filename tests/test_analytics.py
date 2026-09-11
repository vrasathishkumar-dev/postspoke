"""Tests for the analytics module."""

import pytest
from datetime import datetime
from postspoke.analytics import AnalyticsEngine, PostMetrics


def test_add_post_and_generate_summary():
    """Test that posts can be added and summarized."""
    engine = AnalyticsEngine()
    engine.add_post(
        post_time=datetime(2026, 9, 10, 10, 0, 0),
        reach=150,
        clicks=45,
        conversions=8
    )
    engine.add_post(
        post_time=datetime(2026, 9, 10, 11, 0, 0),
        reach=200,
        clicks=120,
        conversions=15
    )
    summary = engine.generate_summary_report()
    assert summary["total_posts"] == 2
    assert summary["total_reach"] == 350
    assert summary["total_clicks"] == 165
    assert summary["total_conversions"] == 23
    assert summary["avg_ctr"] == pytest.approx(0.45, abs=0.001)
    assert summary["avg_conversion_rate"] == pytest.approx(0.06417, abs=0.001)


def test_get_posts_by_date_range():
    """Test filtering posts by date range."""
    engine = AnalyticsEngine()
    engine.add_post(
        post_time=datetime(2026, 9, 10, 10, 0, 0),
        reach=100,
        clicks=30,
        conversions=3
    )
    engine.add_post(
        post_time=datetime(2026, 9, 11, 12, 0, 0),
        reach=250,
        clicks=80,
        conversions=12
    )
    range_start = datetime(2026, 9, 10, 0, 0, 0)
    range_end = datetime(2026, 9, 12, 0, 0, 0)
    filtered = engine.get_posts_by_date_range(range_start, range_end)
    assert len(filtered) == 2
    assert filtered[0].post_time.date() == datetime(2026, 9, 10).date()
    assert filtered[1].post_time.date() == datetime(2026, 9, 11).date()


def test_click_through_rate_calculation():
    """Test CTR calculation."""
    engine = AnalyticsEngine()
    zero_reach_post = PostMetrics(
        post_time=datetime(2026, 9, 10, 10, 0, 0),
        reach=0,
        clicks=10,
        conversions=1
    )
    assert zero_reach_post.click_through_rate == 0.0
    assert zero_reach_post.conversion_rate == 0.0
    normal_post = PostMetrics(
        post_time=datetime(2026, 9, 10, 10, 0, 0),
        reach=100,
        clicks=25,
        conversions=3
    )
    assert normal_post.click_through_rate == 0.25
    assert normal_post.conversion_rate == 0.03
