
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from bank_sim.database import Base

class Client(Base):
    __tablename__ = "clients"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    accounts = relationship("Account", back_populates="client")
    def __repr__(self):
        return f"<Client id={self.id} name={self.name}>"
