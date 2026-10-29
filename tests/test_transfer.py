import allure
import pytest

from bank_account import BankAccount


@allure.feature("Transfer")
@allure.title("TC12 - Transfer money with 1% fee")
@allure.severity(allure.severity_level.BLOCKER)
def test_TC12_transfer_valid(account, other_account):
    with allure.step("An transfers 500,000 to Binh"):
        account.transfer(other_account, 500_000)
    with allure.step("An pays 500,000 + 5,000 fee"):
        assert account.balance == 1_000_000 - 505_000
    with allure.step("Binh receives 500,000"):
        assert other_account.balance == 500_000


@allure.feature("Transfer")
@allure.title("TC13/TC14/TC15 - Transfer fee: {amount} -> {expected_fee}")
@pytest.mark.parametrize("amount, expected_fee", [
    pytest.param(50_000,    1_000,  id="TC13-small_amount_min_fee"),
    pytest.param(100_000,   1_000,  id="TC14-boundary_1pct_equals_min"),
    pytest.param(2_000_000, 20_000, id="TC15-large_amount_1pct"),
])
def test_transfer_fee(amount, expected_fee):
    assert BankAccount.transfer_fee(amount) == expected_fee


@allure.feature("Transfer")
@allure.title("TC16 - Transfer when balance does not cover the fee")
def test_TC16_transfer_not_enough_for_fee(account, other_account):
    with pytest.raises(ValueError, match="Insufficient balance"):
        account.transfer(other_account, 1_000_000)     # cần 1.010.000đ
    assert account.balance == 1_000_000
    assert other_account.balance == 0


@allure.feature("Transfer")
@allure.title("TC17 - Transfer to the same account")
def test_TC17_transfer_to_self(account):
    with pytest.raises(ValueError, match="same account"):
        account.transfer(account, 100_000)


@allure.feature("Locked account")
@allure.title("TC18 - Locked account cannot deposit")
@allure.severity(allure.severity_level.CRITICAL)
def test_TC18_locked_account_cannot_deposit(account):
    account.lock()
    with pytest.raises(PermissionError, match="locked"):
        account.deposit(100_000)


@allure.feature("Locked account")
@allure.title("TC19 - Cannot transfer to a locked account")
def test_TC19_transfer_to_locked_account(account, other_account):
    other_account.lock()
    with pytest.raises(PermissionError, match="Target account is locked"):
        account.transfer(other_account, 100_000)
    assert account.balance == 1_000_000


@allure.feature("History")
@allure.title("TC20 - Transaction history is recorded")
def test_TC20_history(account, other_account):
    account.deposit(100_000)
    account.withdraw(50_000)
    account.transfer(other_account, 200_000)
    assert account.history == [("deposit", 100_000), ("withdraw", 50_000), ("transfer_out", 200_000)]
    assert other_account.history == [("transfer_in", 200_000)]