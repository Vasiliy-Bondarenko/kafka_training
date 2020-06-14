import faust
from faker import Faker

fake = Faker()


class Trade(faust.Record):
    id: str
    user_id: str
    amount: str
    type: str
    trade_pair: str

    def __str__(self):
        return f"{self.id}: from: {self.user_id} amount: {self.amount} type: {self.type} pair: {self.trade_pair}"

    @staticmethod
    def fake(users_id_up_to=10):
        return Trade(
            id=str(fake.uuid4()),
            user_id=str(fake.random_int(min=1, max=users_id_up_to)),
            amount=fake.random_int(min=1, max=100000),
            type=fake.random_element(elements=("BUY", "SELL")),
            trade_pair="BTC-USD",
        )
