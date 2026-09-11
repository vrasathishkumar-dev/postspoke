from datetime import datetime
from typing import List, Dict, Any
import json


class PostMetrics:
    def __init__(
        self,
        post_id: str,
        scheduled_time: datetime,
        reach: int,
        clicks: int,
        conversions: int,
    ):
        if reach < 0:
            raise ValueError("reach must be non-negative")
        if clicks < 0:
            raise ValueError("clicks must be non-negative")
        if conversions < 0:
            raise ValueError("conversions must be non-negative")
        if clicks > reach:
            raise ValueError("clicks cannot exceed reach")
        if conversions > clicks:
            raise ValueError("conversions cannot exceed clicks")

        self.post_id = post_id
        self.scheduled_time = scheduled_time
        self.reach = reach
        self.clicks = clicks
        self.conversions = conversions

    @property
    def ctr(self) -> float:
        if self.reach == 0:
            return 0.0
        return (self.clicks / self.reach) * 100

    @property
    def conversion_rate(self) -> float:
        if self.clicks == 0:
            return 0.0
        return (self.conversions / self.clicks) * 100


def aggregate_metrics(posts: List[PostMetrics]) -> Dict[str, Any]:
    if not posts:
        return {
            "total_reach": 0,
            "total_clicks": 0,
            "total_conversions": 0,
            "avg_ctr": 0.0,
            "avg_conversion_rate": 0.0,
            "post_count": 0,
        }

    total_reach = sum(p.reach for p in posts)
    total_clicks = sum(p.clicks for p in posts)
    total_conversions = sum(p.conversions for p in posts)
    post_count = len(posts)

    avg_ctr = sum(p.ctr for p in posts) / post_count if post_count > 0 else 0.0
    avg_conversion_rate = (
        sum(p.conversion_rate for p in posts) / post_count if post_count > 0 else 0.0
    )

    return {
        "total_reach": total_reach,
        "total_clicks": total_clicks,
        "total_conversions": total_conversions,
        "avg_ctr": avg_ctr,
        "avg_conversion_rate": avg_conversion_rate,
        "post_count": post_count,
    }


def generate_json_report(posts: List[PostMetrics], output_path: str) -> None:
    data = {
        "total_reach": sum(p.reach for p in posts),
        "total_clicks": sum(p.clicks for p in posts),
        "total_conversions": sum(p.conversions for p in posts),
        "posts": [
            {
                "post_id": p.post_id,
                "scheduled_time": p.scheduled_time.isoformat(),
                "reach": p.reach,
                "clicks": p.clicks,
                "conversions": p.conversions,
                "ctr": p.ctr,
                "conversion_rate": p.conversion_rate,
            }
            for p in posts
        ],
    }
    with open(output_path, "w") as f:
        json.dump(data, f, indent=2)


def generate_cli_summary(posts: List[PostMetrics]) -> None:
    if not posts:
        print("No posts to summarize.")
        return

    agg = aggregate_metrics(posts)
    print(f"Total Reach: {agg['total_reach']}")
    print(f"Total Clicks: {agg['total_clicks']}")
    print(f"Total Conversions: {agg['total_conversions']}")
    print(f"Average CTR: {agg['avg_ctr']:.1f}%")
    print(f"Average Conversion Rate: {agg['avg_conversion_rate']:.1f}%")
