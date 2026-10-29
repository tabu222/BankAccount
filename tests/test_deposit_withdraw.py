import allure
import pytest

from bank_account import BankAccount


@allure.feature("Create account")
@allure.title("TC01 - Create account with valid data")
@allure.severity(allure.severity_level.CRITICAL)
def test_TC01_create_account():
    acc = BankAccount("Nguyen Van An", 500_000)
    assert acc.owner == "Nguyen Van An"
    assert acc.balance == 500_000


@allure.feature("Create account")
@allure.title("TC02 - Create account with empty owner name")
def test_TC02_create_account_empty_owner():
    with pytest.raises(ValueError, match="Owner name is required"):
        BankAccount("", 0)


@allure.feature("Create account")
@allure.title("TC03 - Create account with negative balance")
def test_TC03_create_account_negative_balance():
    with pytest.raises(ValueError, match="cannot be negative"):
        BankAccount("Nguyen Van An", -1)


@allure.feature("Deposit")
@allure.title("TC04 - Deposit a valid amount")
@allure.severity(allure.severity_level.CRITICAL)
def test_TC04_deposit_valid(account):
    with allure.step("Deposit 200,000"):
        account.deposit(200_000)
    with allure.step("Check balance is 1,200,000"):
        assert account.balance == 1_200_000


@allure.feature("Deposit")
@allure.title("TC05/TC06 - Deposit an invalid amount: {amount}")
@pytest.mark.parametrize("amount", [
    pytest.param(0,      id="TC05-amount_0"),
    pytest.param(-5_000, id="TC06-amount_negative"),
])
def test_deposit_invalid_amount(account, amount):
    with pytest.raises(ValueError, match="greater than 0"):
        account.deposit(amount)
    assert account.balance == 1_000_000


@allure.feature("Withdraw")
@allure.title("TC07 - Withdraw a valid amount")
@allure.severity(allure.severity_level.CRITICAL)
def test_TC07_withdraw_valid(account):
    account.withdraw(300_000)
    assert account.balance == 700_000


@allure.feature("Withdraw")
@allure.title("TC08 - Withdraw the whole balance")
def test_TC08_withdraw_all(account):
    account.withdraw(1_000_000)
    assert account.balance == 0


@allure.feature("Withdraw")
@allure.title("TC09 - Withdraw more than the balance")
def test_TC09_withdraw_more_than_balance(account):
    with pytest.raises(ValueError, match="Insufficient balance"):
        account.withdraw(1_000_001)
    assert account.balance == 1_000_000


@allure.feature("Withdraw")
@allure.title("TC10/TC11 - Withdraw limit boundary: {amount}")
@pytest.mark.parametrize("amount, allowed", [
    pytest.param(5_000_000, True,  id="TC10-exactly_5M"),
    pytest.param(5_000_001, False, id="TC11-over_5M"),
])
def test_withdraw_limit_boundary(amount, allowed):
    acc = BankAccount("Le Khanh Linh", 10_000_000)
    if allowed:
        acc.withdraw(amount)
        assert acc.balance == 10_000_000 - amount
    else:
        with pytest.raises(ValueError, match="5,000,000"):
            acc.withdraw(amount)