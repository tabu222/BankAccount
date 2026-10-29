"""
Chương trình mô phỏng ngân hàng chạy trên console.
Chạy:  py main.py
"""
from bank_account import BankAccount


def main():
    an = BankAccount("Nguyen Van An", 2_000_000)
    binh = BankAccount("Tran Thi Binh", 500_000)
    print(f"Ban dau : An = {an.balance:,}d | Binh = {binh.balance:,}d")

    an.deposit(1_000_000)
    print(f"An nap 1,000,000d        -> An = {an.balance:,}d")

    an.withdraw(500_000)
    print(f"An rut 500,000d          -> An = {an.balance:,}d")

    an.transfer(binh, 1_000_000)
    fee = BankAccount.transfer_fee(1_000_000)
    print(f"An chuyen 1,000,000d cho Binh (phi {fee:,}d)")
    print(f"                         -> An = {an.balance:,}d | Binh = {binh.balance:,}d")

    try:
        binh.withdraw(10_000_000)
    except ValueError as error:
        print(f"Binh rut 10,000,000d     -> LOI: {error}")


if __name__ == "__main__":
    main()