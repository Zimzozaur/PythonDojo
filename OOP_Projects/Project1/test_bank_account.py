import pytest

from bank_account import (
    BankRegisters, BankAccount,
    Transaction
)


#################
# Testing Setup #
#################


@pytest.fixture(autouse=True)
def reset_settings():
    BankAccount._user_id = 1

    _bank = BankRegisters()
    _bank._interest_rate = 0.05
    _bank._user_registry = {}
    _bank._transaction_registry = {}

    Transaction._transaction_id = 1


####################
# Testing Fixtures #
####################


@pytest.fixture
def bank_user():
    return {
        'first_name': 'Mario',
        'last_name': 'Miyamoto',
        'time_zone': +8
    }


###############################
# Testing BankAccountRegistry #
###############################


def test_transaction_id_increase(bank_user):
    # Setup
    user1 = BankAccount(**bank_user)
    user2 = BankAccount(**bank_user)
    trans1 = user1.deposit(1000)
    trans2 = user2.deposit(2000)

    assert trans1.id == 1
    assert trans2.id == 2


###############################
# Testing BankAccountRegistry #
###############################


def test_is_back_account_registry_true_singleton():
    instance1 = BankRegisters()
    instance2 = BankRegisters()
    assert instance1 is instance2


def test_add_user():
    instance = BankRegisters()
    instance.add_user(1, 1)
    instance.add_user(2, 2)
    assert len(instance._user_registry) == 2


def test_get_user():
    instance = BankRegisters()
    instance.add_user(1, 1)
    with pytest.raises(ValueError, match='User ID is not valid'):
        instance.get_user(2)
    assert instance.get_user(1) == 1


def test_change_interest_rate():
    bank = BankRegisters()
    with pytest.raises(ValueError, match='Capitalization cannot be lower than 0'):
        bank.set_interest_rate(-5.0)
    bank.set_interest_rate(0.06)
    assert bank._interest_rate == 0.06


def test_capitalization(bank_user):
    bank = BankRegisters()
    user1 = BankAccount(**bank_user)
    user2 = BankAccount(**bank_user)

    user1.deposit(100)
    user2.deposit(300)
    bank.capitalize()

    assert int(user1.get_balance()) == 105
    assert int(user2.get_balance()) == 315

    assert len(bank._transaction_registry) == 4


def test_transaction_registry(bank_user):
    user = BankAccount(**bank_user)
    bank = user._bank
    transaction = user.deposit(100)
    assert bank._transaction_registry[1] is transaction

#######################
# Testing BankAccount #
#######################


def test_bank_account_initialization(bank_user):
    account = BankAccount(**bank_user)
    assert account.first_name == bank_user['first_name']
    assert account.last_name == bank_user['last_name']
    assert account.time_zone == bank_user['time_zone']
    assert account._id == 1

    # Check registering of instance
    assert account._bank.get_user(1) is account


def test_id_increment(bank_user):
    account1 = BankAccount(**bank_user)
    account2 = BankAccount(**bank_user)

    assert account1._user_id == 3 and account2._user_id == 3
    assert account1._id == 1 and account2._id == 2
    assert account1._bank.get_user(1) is account1
    assert account2._bank.get_user(2) is account2


def test_getting_account_by_id(bank_user):
    account1 = BankAccount(**bank_user)
    account2 = BankAccount(**bank_user)

    assert account1.get_account_by_id(1) == account1
    assert account1.get_account_by_id(2) == account2

    assert account2.get_account_by_id(2) == account2
    assert account2.get_account_by_id(1) == account1


def test_depositing(bank_user):
    account1 = BankAccount(**bank_user)
    assert account1.get_balance() == 0  # Default balance check
    transaction = account1.deposit(100)
    assert account1.get_balance() == 100  # Balance Check
    # Transaction Check
    assert transaction._id == 1
    assert transaction.transaction_type == 'D'
    assert transaction.transaction_value == 100
    assert transaction.to_account == account1._id
    assert transaction.from_account is None


def test_false_deposit(bank_user):
    account1 = BankAccount(**bank_user)
    with pytest.raises(ValueError, match='Despotie cannot be lower then 0'):
        account1.deposit(-1)
