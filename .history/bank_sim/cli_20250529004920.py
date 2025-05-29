
import click
from rich.console import Console
from rich.table import Table
from rich.logging import RichHandler
import logging

from bank_sim.services import ClientService, AccountService, BankQueue
from bank_sim import database

queue = BankQueue()
console = Console()
logging.basicConfig(level=logging.INFO, handlers=[RichHandler()])


@click.group()
def cli():
    """Bank Simulation CLI (150%)."""


@cli.command()
@click.argument("name")
def register(name):
    client = ClientService.register(name)
    console.print(f"[bold green]Клиент зарегистрирован:[/] id={client.id}, name={client.name}")


@cli.command("open")
@click.argument("client_id", type=int)
def open_account(client_id):
    account = AccountService.open_account(client_id)
    console.print(f"[cyan]Счёт открыт:[/] id={account.id} (client {client_id})")


@cli.command()
@click.argument("client_id", type=int)
def enqueue(client_id):
    queue.enqueue(client_id)
    console.print(f"Клиент {client_id} встал в очередь. Длина: {len(queue)}")


@cli.command()
def queue_list():
    if len(queue) == 0:
        console.print("[yellow]Очередь пуста[/]")
    else:
        console.print("Текущая очередь:", queue.list())


@cli.command()
def serve():
    client_id = queue.serve_next()
    if client_id is None:
        console.print("[yellow]Очередь пуста[/]")
    else:
        console.print(f"[bold]Обслуживание клиента {client_id}[/]")    


@cli.command()
@click.argument("account_id", type=int)
@click.argument("amount", type=float)
def deposit(account_id, amount):
    balance = AccountService.deposit(account_id, amount)
    console.print(f"Баланс счёта {account_id}: {balance:,.2f}")


@cli.command()
@click.argument("account_id", type=int)
@click.argument("amount", type=float)
def withdraw(account_id, amount):
    try:
        balance = AccountService.withdraw(account_id, amount)
        console.print(f"Баланс счёта {account_id}: {balance:,.2f}")
    except ValueError as e:
        console.print(f"[red]Ошибка:[/] {e}")


@cli.command()
@click.argument("from_account", type=int)
@click.argument("to_account", type=int)
@click.argument("amount", type=float)
def transfer(from_account, to_account, amount):
    try:
        bal_from, bal_to = AccountService.transfer(from_account, to_account, amount)
        console.print(f"Баланс отправителя: {bal_from:,.2f}; получателя: {bal_to:,.2f}")
    except ValueError as e:
        console.print(f"[red]Ошибка:[/] {e}")

@cli.command()
def shell():
    """Интерактивный режим (REPL)."""
    console.print("[bold cyan]Интерактивный режим. Введите 'exit' для выхода.[/]")
    while True:
        try:
            cmd = input("bank> ")
        except (KeyboardInterrupt, EOFError):
            console.print("\n[bold]До свидания![/]")
            break
        if cmd.strip().lower() in {"exit", "quit"}:
            break
        if not cmd.strip():
            continue
        try:
            tokens = shlex.split(cmd)
            # standalone_mode=False → не завершаем процесс после выполнения
            cli(tokens, standalone_mode=False)
        except SystemExit:
            # подавляем стандартный выход Click при --help/ошибках
            pass
        except Exception as exc:
            console.print(f"[red]Ошибка:[/] {exc}")

@cli.command()
@click.argument("account_id", type=int)
def history(account_id):
    txns = AccountService.history(account_id)
    if not txns:
        console.print("[italic]История пуста[/]")
        return
    table = Table(title=f"История счёта {account_id}")
    table.add_column("⏱ Дата/время")
    table.add_column("Тип")
    table.add_column("Сумма", justify="right")
    table.add_column("От", justify="right")
    table.add_column("Кому", justify="right")
    for t in txns:
        table.add_row(
            str(t.timestamp)[:19],
            t.type,
            f"{t.amount:,.2f}",
            str(t.from_account_id or ""),
            str(t.to_account_id or ""),
        )
    console.print(table)


@cli.command()
def initdb():
    database.init_db()
    console.print("[green]База данных инициализирована[/]")
