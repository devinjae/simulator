from typing import Dict, List, Optional

import redis.asyncio as redis


class Leaderboard:
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client

        # Overall leaderboard -> ZSET (sorted set)
        self.LEADERBOARD_KEY = "leaderboard:{competition_id}"

    async def update_user_pnl(
        self, competition_id: str, user_id: str, pnl: float
    ) -> None:
        # will be called from USER CLASS
        leaderboard_key = self.LEADERBOARD_KEY.format(competition_id=competition_id)
        await self.redis.zadd(leaderboard_key, {user_id: pnl})

    async def get_leaderboard(
        self, competition_id: str, limit: int = 100  # can be used to get top N
    ) -> List[Dict[str, float]]:
        leaderboard_key = self.LEADERBOARD_KEY.format(competition_id=competition_id)

        # ZREVRANGE to get descending based on scores
        leaderboard = await self.redis.zrevrange(
            leaderboard_key, 0, limit - 1, withscores=True
        )
        return [
            {"user_id": user_id.decode(), "pnl": float(score)}
            for user_id, score in leaderboard
        ]

    async def get_user_rank(self, competition_id: str, user_id: str) -> Optional[int]:
        leaderboard_key = self.LEADERBOARD_KEY.format(competition_id=competition_id)
        rank = await self.redis.zrevrank(leaderboard_key, user_id)
        return rank + 1 if rank is not None else None
