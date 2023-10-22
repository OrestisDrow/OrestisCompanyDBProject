import subprocess
import sqlite3
import click

"""Guards in order to check if the db is initialized and/or populated"""
def db_initialized():
    """Check if the database has been initialized."""
    try:
        with sqlite3.connect('/app/data/orestiscompanydb.sqlite') as conn:
            cursor = conn.cursor()
            tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
            # Assuming a critical table that should exist after initialization is 'Sales'
            return any('Sales' in table for table in tables)
    except sqlite3.OperationalError:
        return False

def db_populated():
    """Check if the database has been populated."""
    try:
        with sqlite3.connect('/app/data/orestiscompanydb.sqlite') as conn:
            cursor = conn.cursor()
            # Ensure the 'Customers' table exists before querying
            tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
            if not any('Customers' in table for table in tables):
                return False
            # Count the records in 'Customers' table
            count = cursor.execute("SELECT COUNT(*) FROM Customers;").fetchone()[0]
            return count > 0
    except sqlite3.OperationalError:
        return False



@click.group()
@click.pass_context
def cli(ctx):
    pass

@cli.command()
@click.pass_context  # This decorator ensures that ctx is passed to the function
def repl(ctx):
    """Start a REPL session."""
    click.echo("Welcome to the orestiscompany CLI!")
    click.echo("Here are the available commands:")
    click.echo("  initialize_db   - Initialize the database.")
    click.echo("  populate_db     - Populate the database with data.")
    click.echo("  reset_db        - Reset and repopulate the database.")
    click.echo("  exit or quit    - Exit the CLI.")
    click.echo("")
    while True:
        command = input('orestiscompany> ')
        if command == 'exit' or command == 'quit':
            break
        elif command == 'initialize_db':
            ctx.invoke(initialize_db)
        elif command == 'populate_db':
            ctx.invoke(populate_db)
        elif command == 'reset_db':
            ctx.invoke(reset_db)
        else:
            click.echo(f"Unknown command: {command}")



@cli.command()
def initialize_db():
    """Initialize the database."""
    try:
        # Execute the initialize_db.sh script
        subprocess.run(["/app/scripts/initialize_db.sh"], check=True)
        click.echo("Database initialized successfully!")
    except subprocess.CalledProcessError:
        click.echo("An error occurred while initializing the database.")

@cli.command()
def populate_db():
    """Populate the database with data."""
    if not db_initialized():
        click.echo("Error: The database has not been initialized. Please run 'initialize_db' first.")
        return
    try:
        # Execute the populate_db.sh script
        subprocess.run(["/app/scripts/populate_db.sh"], check=True)
        click.echo("Database populated successfully!")
    except subprocess.CalledProcessError:
        click.echo("An error occurred while populating the database.")

@cli.command()
def reset_db():
    """Reset and repopulate the database."""
    if not db_populated():
        click.echo("Error: The database has not been populated. Please run 'populate_db' first.")
        return
    confirmation = click.confirm("Are you sure you want to reset and repopulate the database? This action is irreversible.", abort=True)
    if confirmation:
        try:
            # Execute the reset_db.sh script
            subprocess.run(["/app/scripts/reset_db.sh"], check=True)
            click.echo("Database reset and repopulated successfully!")
        except subprocess.CalledProcessError:
            click.echo("An error occurred while resetting the database.")

if __name__ == "__main__":
    cli()
