
from sqlalchemy import Integer, ForeignKey, Numeric, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from bank_sim.database import Base

class Transaction(Base):
    __tablename__ = "transactions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    timestamp: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now())
    type: Mapped[str] = mapped_column(String(20))
    amount: Mapped[float] = mapped_column(Numeric(12, 2))
    from_account_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("accounts.id"), nullable=True)
    to_account_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("accounts.id"), nullable=True)
    from_account = relationship("Account", foreign_keys=[from_account_id], back_populates="transactions_from")
    to_account = relationship("Account", foreign_keys=[to_account_id], back_populates="transactions_to")
