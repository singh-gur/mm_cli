from datetime import datetime, timedelta

import click

from ..utils import write_csv, format_date
from ..commands.auth import get_authenticated_client


@click.group()
def export():
    """Export data to CSV files"""
    pass


@export.command()
@click.option("--start-date", type=click.DateTime(formats=["%Y-%m-%d"]),
              default=lambda: datetime.now() - timedelta(days=30),
              help="Start date (YYYY-MM-DD), defaults to 30 days ago")
@click.option("--end-date", type=click.DateTime(formats=["%Y-%m-%d"]),
              default=lambda: datetime.now(),
              help="End date (YYYY-MM-DD), defaults to today")
@click.option("--output", "-o", default=".", help="Output directory")
@click.option("--filename", default="transactions.csv", help="Output filename")
def transactions(start_date, end_date, output, filename):
    """Export transactions to CSV"""
    try:
        mm = get_authenticated_client()

        click.echo(f"Fetching transactions from {start_date.date()} to {end_date.date()}...")

        transactions_data = mm.get_transactions(
            start_date=start_date.isoformat(),
            end_date=end_date.isoformat()
        )

        if not transactions_data:
            click.echo("No transactions found for the specified date range")
            return

        # Process transactions for CSV export
        processed_transactions = []
        for transaction in transactions_data:
            processed = {
                'id': transaction.get('id'),
                'date': format_date(transaction.get('date')),
                'description': transaction.get('description', ''),
                'merchant': transaction.get('merchant', {}).get('name', '') if transaction.get('merchant') else '',
                'amount': transaction.get('amount', 0),
                'currency': transaction.get('currency', 'USD'),
                'category': transaction.get('category', {}).get('name', '') if transaction.get('category') else '',
                'account': transaction.get('account', {}).get('displayName', '') if transaction.get('account') else '',
                'account_type': transaction.get('account', {}).get('type', '') if transaction.get('account') else '',
                'pending': transaction.get('pending', False),
                'notes': transaction.get('notes', ''),
                'tags': ', '.join([tag.get('name', '') for tag in transaction.get('tags', [])])
            }
            processed_transactions.append(processed)

        filepath = write_csv(processed_transactions, filename, output)
        click.echo(f"✓ Exported {len(processed_transactions)} transactions to {filepath}")

    except Exception as e:
        click.echo(f"✗ Export failed: {e}", err=True)
        raise click.Abort()


@export.command()
@click.option("--output", "-o", default=".", help="Output directory")
@click.option("--filename", default="accounts.csv", help="Output filename")
def accounts(output, filename):
    """Export accounts to CSV"""
    try:
        mm = get_authenticated_client()

        click.echo("Fetching accounts...")

        accounts_data = mm.get_accounts()

        if not accounts_data:
            click.echo("No accounts found")
            return

        # Process accounts for CSV export
        processed_accounts = []
        for account in accounts_data:
            processed = {
                'id': account.get('id'),
                'name': account.get('displayName', ''),
                'type': account.get('type', ''),
                'subtype': account.get('subtype', ''),
                'balance': account.get('currentBalance', 0),
                'currency': account.get('currency', 'USD'),
                'institution': account.get('institution', {}).get('name', '') if account.get('institution') else '',
                'is_active': account.get('isActive', True),
                'is_hidden': account.get('isHidden', False),
                'created_at': format_date(account.get('createdAt', '')),
                'updated_at': format_date(account.get('updatedAt', ''))
            }
            processed_accounts.append(processed)

        filepath = write_csv(processed_accounts, filename, output)
        click.echo(f"✓ Exported {len(processed_accounts)} accounts to {filepath}")

    except Exception as e:
        click.echo(f"✗ Export failed: {e}", err=True)
        raise click.Abort()


@export.command()
@click.option("--output", "-o", default=".", help="Output directory")
@click.option("--filename", default="budgets.csv", help="Output filename")
def budgets(output, filename):
    """Export budgets to CSV"""
    try:
        mm = get_authenticated_client()

        click.echo("Fetching budgets...")

        budgets_data = mm.get_budgets()

        if not budgets_data:
            click.echo("No budgets found")
            return

        # Process budgets for CSV export
        processed_budgets = []
        for budget in budgets_data:
            processed = {
                'id': budget.get('id'),
                'name': budget.get('name', ''),
                'amount': budget.get('amount', 0),
                'spent': budget.get('spent', 0),
                'remaining': budget.get('remaining', 0),
                'category': budget.get('category', {}).get('name', '') if budget.get('category') else '',
                'period': budget.get('period', ''),
                'is_active': budget.get('isActive', True)
            }
            processed_budgets.append(processed)

        filepath = write_csv(processed_budgets, filename, output)
        click.echo(f"✓ Exported {len(processed_budgets)} budgets to {filepath}")

    except Exception as e:
        click.echo(f"✗ Export failed: {e}", err=True)
        raise click.Abort()


@export.command()
@click.option("--output", "-o", default=".", help="Output directory")
@click.option("--filename", default="categories.csv", help="Output filename")
def categories(output, filename):
    """Export categories to CSV"""
    try:
        mm = get_authenticated_client()

        click.echo("Fetching categories...")

        categories_data = mm.get_categories()

        if not categories_data:
            click.echo("No categories found")
            return

        # Process categories for CSV export
        processed_categories = []
        for category in categories_data:
            processed = {
                'id': category.get('id'),
                'name': category.get('name', ''),
                'icon': category.get('icon', ''),
                'color': category.get('color', ''),
                'order': category.get('order', 0),
                'is_income': category.get('isIncome', False),
                'is_transfer': category.get('isTransfer', False),
                'is_hidden': category.get('isHidden', False)
            }
            processed_categories.append(processed)

        filepath = write_csv(processed_categories, filename, output)
        click.echo(f"✓ Exported {len(processed_categories)} categories to {filepath}")

    except Exception as e:
        click.echo(f"✗ Export failed: {e}", err=True)
        raise click.Abort()
