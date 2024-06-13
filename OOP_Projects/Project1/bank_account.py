from typing import Dict, Literal
from datetime import datetime


class TimeZone:
    pass


class Transaction:
    _transaction_id = 1

    def __init__(
        self,
        transaction_type: Literal['D', 'W', 'I', 'X'],
        time: TimeZone,
        transaction_value: float,
        to_account: int,
        from_account: int | None = None,
    ):
        self.transaction_type: Literal['D', 'W', 'I', 'X'] = transaction_type
        self.from_account: int = from_account
        self.to_account: int = to_account
        self.time: TimeZone = time
        self._id: int = self.get_increase_transaction_id()
        self.transaction_value: float = transaction_value

    @classmethod
    def get_increase_transaction_id(cls) -> int:
        transaction_id = cls._transaction_id
        cls._transaction_id += 1
        return transaction_id

    def get_transaction_id(self):
        return self._id

    @property
    def id(self):
        return self._id


class BankRegisters:
    _instance = None
    _interest_rate = 0.05
    _user_registry: Dict[int, 'BankAccount'] = {}
    _transaction_registry: Dict[int, Transaction] = {}

    def __new__(cls) -> 'BankRegisters':
        if cls._instance is None:
            cls._instance = super(cls, cls).__new__(cls)
        return cls._instance

    def add_user(self, user_id: int, account_instance) -> None:
        self._user_registry[user_id] = account_instance

    def get_user(self, user_id: int) -> 'BankAccount':
        if user_id not in self._user_registry:
            raise ValueError('User ID is not valid')
        return self._user_registry.get(user_id)

    def capitalize(self):
        for account in self._user_registry.values():
            account.deposit(account.get_balance() * self._interest_rate)

    def set_interest_rate(self, percentage: float) -> None:
        if percentage < 0:
            raise ValueError('Capitalization cannot be lower than 0')
        self._interest_rate = percentage

    def register_transaction(self, transaction: Transaction):
        self._transaction_registry[transaction.id] = transaction

    @property
    def transaction_registry(self):
        return self._transaction_registry


class BankAccount:
    _bank: BankRegisters = BankRegisters()
    _user_id = 1

    @classmethod
    def get_and_increase_user_id(cls):
        user_id = cls._user_id
        cls._user_id += 1
        return user_id

    def __init__(
            self,
            first_name: str,
            last_name: str,
            time_zone: int = 0
    ) -> None:
        # Adding account to registry
        self._id = self.get_and_increase_user_id()
        self._bank.add_user(self._id, self)

        # Setting account properties
        self.first_name: str = first_name
        self.last_name: str = last_name
        self.time_zone: int = time_zone
        self._balance: float = 0

    def get_account_by_id(self, account_id: int):
        result = self._bank.get_user(account_id)
        if not result:
            raise ValueError('Input correct account id')
        return result

    def get_balance(self) -> float:
        return self._balance

    def deposit(self, value: float) -> Transaction:
        """Add value to your balance"""
        if value < 0:
            raise ValueError('Despotie cannot be lower then 0')

        self._balance += value
        transaction = Transaction(
            transaction_type='D',
            to_account=self._id,
            time=TimeZone(),
            transaction_value=value
        )
        self._bank.register_transaction(transaction)
        return transaction

    def withdraw(self, value, to_account) -> Transaction:
        if self._balance < value:
            # reject but add to history
            transaction = Transaction(
                transaction_type='X',
                from_account=self._id,
                to_account=to_account,
                time=TimeZone(),
                transaction_value=value
            )
            self._bank.register_transaction(transaction)
            return transaction

        self._balance -= value
        # Add founds to targe account
        self._bank.get_user(to_account).deposit(value)
        transaction = Transaction(
            transaction_type='W',
            from_account=self._id,
            to_account=to_account,
            time=TimeZone(),
            transaction_value=value
        )
        self._bank.register_transaction(transaction)
        return transaction

