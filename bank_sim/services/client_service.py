
from bank_sim.database import SessionLocal
from bank_sim.models import Client

class ClientService:
    @staticmethod
    def register(name: str) -> Client:
        with SessionLocal() as session:
            client = Client(name=name)
            session.add(client)
            session.commit()
            session.refresh(client)
            return client

    @staticmethod
    def get(client_id: int) -> Client | None:
        with SessionLocal() as session:
            return session.get(Client, client_id)
