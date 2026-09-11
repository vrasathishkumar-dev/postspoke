"""Analytics for PostSpoke engagement metrics.

This module tracks post engagement metrics (reach, clicks, conversions)
associated with scheduled posts from the scheduler.
"""

from datetime import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass


@dataclass
class PostMetrics:
    """Metrics for a single post."""
    post_time: datetime
    reach: int = 0
    clicks: int = 0
    conversions: int = 0

    @property
    def click_through_rate(self) -> float:
        """Calculate CTR (clicks / reach)."""
        return (self.clicks / self.reach) if self.reach > 0 else 0.0

    @property
    def conversion_rate(self) -> float:
        """Calculate conversion rate (conversions / reach)."""
        return (self.conversions / self.reach) if self.reach > 0 else 0.0


class AnalyticsEngine:
    """Generate engagement metrics reports from scheduled posts."""

    def __init__(self):
        self.posts: List[PostMetrics] = []

    def add_post(self, post_time: datetime, reach: int = 0,
                 clicks: int = 0, conversions: int = 0):
        """Record metrics for a scheduled post."""
        self.posts.append(PostMetrics(
            post_time=post_time,
            reach=reach,
            clicks=clicks,
            conversions=conversions
        ))

    def get_posts_by_date_range(self, start_date: datetime,
                               end_date: datetime) -> List[PostMetrics]:
        """Filter posts within a date range (inclusive)."""
        return [
            post for post in self.posts
            if start_date <= post.post_time <= end_date
        ]

    def generate_summary_report(self, start_date: Optional[datetime] = None,
                               end_date: Optional[datetime] = None) -> Dict:
        """Generate a summary report of post engagement metrics.

        Args:
            start_date: Optional start date for filtering
            end_date: Optional end date for filtering

        Returns:
            Dictionary containing summary metrics
        """
        posts_to_report = self.posts
        if start_date and end_date:
            posts_to_report = self.get_posts_by_date_range(start_date, end_date)

        if not posts_to_report:
            return {
                "total_posts": 0,
                "total_reach": 0,
                "total_clicks": 0,
                "total_conversions": 0,
                "avg_ctr": 0.0,
                "avg_conversion_rate": 0.0
            }

        total_reach = sum(post.reach for post in posts_to_report)
        total_clicks = sum(post.clicks for post in posts_to_report)
        total_conversions = sum(post.conversions for post in posts_to_report)

        avg_ctr = sum(post.click_through_rate for post in posts_to_report) / len(posts_to_report)
        avg_conversion_rate = sum(post.conversion_rate for post in posts_to_report) / len(posts_to_report)

        return {
            "total_posts": len(posts_to_report),
            "total_reach": total_reach,
            "total_clicks": total_clicks,
            "total_conversions": total_conversions,
            "avg_ctr": avg_ctr,
            "avg_conversion_rate": avg_conversion_rate,
            "posts": [
                {
                    "post_time": post.post_time.isoformat(),
                    "reach": post.reach,
                    "clicks": post.clicks,
                    "conversions": post.conversions,
                    "ctr": post.click_through_rate,
                    "conversion_rate": post.conversion_rate
                }
                for post in posts_to_report
            ]
        }

    def generate_json_report(self, start_date: Optional[datetime] = None,
                            end_date: Optional[datetime] = None) -> str:
        """Generate a JSON-formatted report."""
        import json
        report = self.generate_summary_report(start_date, end_date)
        return json.dumps(report, indent=2, default=str)

    def generate_cli_table(self, start_date: Optional[datetime] = None,
                          end_date: Optional[datetime] = None) -> str:
        """Generate a CLI-friendly table report."""
        report = self.generate_summary_report(start_date, end_date)

        if report["total_posts"] == 0:
            return "No posts found in the specified date range."

        lines = [
            "Post Engagement Metrics Report",
            "=" * 40,
            f"Total Posts: {report['total_posts']}",
            f"Total Reach: {report['total_reach']:,}",
            f"Total Clicks: {report['total_clicks']:,}",
            f"Total Conversions: {report['total_conversions']:,}",
            f"Average CTR: {report['avg_ctr']:.2%}",
            f"Average Conversion Rate: {report['avg_conversion_rate']:.2%}",
            "",
            "Post Details:",
            "-" * 40
        ]

        for post in report["posts"]:
            lines.append(
                f"{post['post_time']} | Reach: {post['reach']:,} | "
                f"Clicks: {post['clicks']:,} | Conv: {post['conversions']} | "
                f"CTR: {post['ctr']:.2%} | Conv Rate: {post['conversion_rate']:.2%}"
            )

        return "\n".join(lines)