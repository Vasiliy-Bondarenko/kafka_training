from trade import Trade
from user import User


class EnrichedTrade(Trade):
    user: User
