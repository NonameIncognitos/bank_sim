
from sqlalchemy import Integer, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from bank_sim.database import Base

class Account(Base):
    __tablename__ = "accounts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id"), nullable=False)
    balance: Mapped[float] = mapped_column(Numeric(12, 2), default=0)
    client = relationship("Client", back_populates="accounts")
    transactions_from = relationship("Transaction", back_populates="from_account", foreign_keys="[Transaction.from_account_id]")
    transactions_to = relationship("Transaction", back_populates="to_account", foreign_keys="[Transaction.to_account_id]")
    def __repr__(self):
        return f"<Account id={self.id} balance={self.balance}>"
