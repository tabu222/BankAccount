"""
Tài khoản ngân hàng (Bank Account) - phần mềm được kiểm thử.

Luật nghiệp vụ:
    - Số tiền nạp / rút / chuyển phải > 0
    - Mỗi lần rút tối đa 5.000.000đ
    - Không được rút / chuyển quá số dư
    - Chuyển tiền tới tài khoản khác bị tính phí 1% (tối thiểu 1.000đ)
    - Tài khoản đã khoá thì không được giao dịch
"""

MAX_WITHDRAW = 5_000_000
TRANSFER_FEE_RATE = 0.01
MIN_TRANSFER_FEE = 1_000


class BankAccount:
    def __init__(self, owner, balance=0):
        if not isinstance(owner, str) or not owner.strip():
            raise ValueError("Owner name is required")
        if balance < 0:
            raise ValueError("Initial balance cannot be negative")
        self.owner = owner
        self.balance = balance
        self.is_locked = False
        self.history = []                    # lịch sử giao dịch

    def _check_amount(self, amount):
        if self.is_locked:
            raise PermissionError("Account is locked")
        if amount <= 0:
            raise ValueError("Amount must be greater than 0")

    def deposit(self, amount):
        self._check_amount(amount)
        self.balance += amount
        self.history.append(("deposit", amount))
        return self.balance

    def withdraw(self, amount):
        self._check_amount(amount)
        if amount > MAX_WITHDRAW:
            raise ValueError("Cannot withdraw more than 5,000,000 at once")
        if amount > self.balance:
            raise ValueError("Insufficient balance")
        self.balance -= amount
        self.history.append(("withdraw", amount))
        return self.balance

    @staticmethod
    def transfer_fee(amount):
        return max(int(amount * TRANSFER_FEE_RATE), MIN_TRANSFER_FEE)

    def transfer(self, target, amount):
        self._check_amount(amount)
        if target is self:
            raise ValueError("Cannot transfer to the same account")
        if target.is_locked:
            raise PermissionError("Target account is locked")
        total = amount + self.transfer_fee(amount)
        if total > self.balance:
            raise ValueError("Insufficient balance")
        self.balance -= total
        target.balance += amount
        self.history.append(("transfer_out", amount))
        target.history.append(("transfer_in", amount))
        return self.balance

    def lock(self):
        self.is_locked = True