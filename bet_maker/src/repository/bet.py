from bet_maker.src.utils.repository import SQLAlchemyRepository
from bet_maker.src.models.model import Bet


class BetRepository(SQLAlchemyRepository):
    model = Bet