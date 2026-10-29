import pytest

from bank_account import BankAccount


@pytest.fixture
def account():
    """Tài khoản mới, số dư 1.000.000đ, dùng riêng cho từng test."""
    return BankAccount("Nguyen Van An", 1_000_000)


@pytest.fixture
def other_account():
    """Tài khoản người nhận, số dư 0đ."""
    return BankAccount("Tran Thi Binh", 0)