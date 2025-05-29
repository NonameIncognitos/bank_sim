
from decimal import Decimal
from bank_sim.database import SessionLocal
from bank_sim.models import Account, Transaction

class AccountService:
    @staticmethod
    def open_account(client_id: int) -> Account:
        with SessionLocal() as session:
            acc = Account(client_id=client_id, balance=Decimal(0))
            session.add(acc)
            session.commit()
            session.refresh(acc)
            return acc

    @staticmethod
    def deposit(account_id: int, amount: float) -> float:
        with SessionLocal() as session:
            acc = session.get(Account, account_id)
            if acc is None:
                raise ValueError("Account not found")
            acc.balance += Decimal(amount)
            session.add(Transaction(type="deposit", amount=amount, to_account_id=account_id))
            session.commit()
            return float(acc.balance)

    @staticmethod
    def withdraw(account_id: int, amount: float) -> float:
        with SessionLocal() as session:
            acc = session.get(Account, account_id)
            if acc is None:
                raise ValueError("Account not found")
            if acc.balance < Decimal(amount):
                raise ValueError("Insufficient funds")
            acc.balance -= Decimal(amount)
            session.add(Transaction(type="withdraw", amount=amount, from_account_id=account_id))
            session.commit()
            return float(acc.balance)

    @staticmethod
    def transfer(from_account: int, to_account: int, amount: float) -> tuple[float, float]:
        with SessionLocal() as session:
            src = session.get(Account, from_account)
            dst = session.get(Account, to_account)
            if src is None or dst is None:
                raise ValueError("Account not found")
            if src.balance < Decimal(amount):
                raise ValueError("Insufficient funds")
            src.balance -= Decimal(amount)
            dst.balance += Decimal(amount)
            session.add(Transaction(type="transfer", amount=amount, from_account_id=from_account, to_account_id=to_account))
            session.commit()
            return float(src.balance), float(dst.balance)

    @staticmethod
    def history(account_id: int):
        with SessionLocal() as session:
            return session.execute(
                session.query(Transaction).filter(
                    (Transaction.from_account_id == account_id) | (Transaction.to_account_id == account_id)
                ).order_by(Transaction.timestamp.desc())
            ).scalars().all()
