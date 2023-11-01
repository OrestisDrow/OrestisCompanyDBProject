import subprocess
import sqlite3
import click
#from analytics.basic_analytics import compute_basic_analytics
from datetime import date, datetime

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
    click.echo("-----Setup Commands-----:")
    click.echo("  initialize_db   - Initialize the database.")
    click.echo("  populate_db     - Populate the database with data.")
    click.echo("  reset_db        - Reset and repopulate the database.")
    click.echo("  exit or quit    - Exit the CLI.")
    click.echo("")
    click.echo("-----Pre-process Analytics Commands-----")
    click.echo("  pre_process_analytics start_date end_date -arg              - Pre-process analytics for visualizations.")
    click.echo("  Note:")
    click.echo("    - dates must be between 20210101 and 20211231, default all dates that data exist [2021, 2022]")
    click.echo("    - arg can be b('basic'), i('intermediate') or a('advanced') analytics, default all")
    
    
    while True:
        command_parts = input('orestiscompany> ').split()
        base_command = command_parts[0]
        args = command_parts[1:]

        if base_command == 'exit' or base_command == 'quit':
            break
        elif base_command == 'initialize_db':
            ctx.invoke(initialize_db)
        elif base_command == 'populate_db':
            ctx.invoke(populate_db)
        elif base_command == 'reset_db':
            ctx.invoke(reset_db)
        elif base_command == 'pre_process_analytics':
            start_date = '20210101'
            end_date = '20221231'
            process_basic = process_intermediate = process_advanced = False

            # Check if any args are flags
            for arg in args:
                if arg in ['-b', '-bi', '-ib', '-ba', '-ab']:
                    process_basic = True
                if arg in ['-i', '-bi', '-ib', '-ia', '-ai']:
                    process_intermediate = True
                if arg in ['-a', '-ai', '-ab', '-ia', '-ba']:
                    process_advanced = True

            if not any([process_basic, process_intermediate, process_advanced]):
                process_basic = process_intermediate = process_advanced = True

            if len(args) > 0 and args[0].isdigit():
                start_date = args[0]
            if len(args) > 1 and args[1].isdigit():
                end_date = args[1]

            ctx.invoke(pre_process_analytics, start_date=start_date, end_date=end_date, process_basic=process_basic, process_intermediate=process_intermediate, process_advanced=process_advanced)
        else:
            click.echo(f"Unknown command: {base_command}")




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


def string_to_date(date_str):
    """
    Convert a string in the format "yyyymmdd" to a datetime.date object.
    """
    try:
        return datetime.strptime(date_str, '%Y%m%d').date()
    except ValueError:
        return None

def is_valid_date_range(start_date, end_date):
    """
    Check if the given start_date and end_date are within the year range [2021, 2022].
    """
    min_date = date(2021, 1, 1)
    max_date = date(2022, 12, 31)
    return min_date <= start_date <= max_date and min_date <= end_date <= max_date

@cli.command()
@click.argument('start_date', required=False, default='20210101')
@click.argument('end_date', required=False, default='20221231')
@click.option('--basic', 'process_basic', is_flag=True, default=False, help='Compute basic analytics')
@click.option('--intermediate', 'process_intermediate', is_flag=True, default=False, help='Compute intermediate analytics')
@click.option('--advanced', 'process_advanced', is_flag=True, default=False, help='Compute advanced analytics')
def pre_process_analytics(start_date, end_date, process_basic, process_intermediate, process_advanced):
    # Check if the database is initialized and populated
    if not db_initialized():
        click.echo("The database hasn't been initialized. Please initialize it before pre-processing analytics.")
        return
    if not db_populated():
        click.echo("The database hasn't been populated. Please populate it before pre-processing analytics.")
        return
    
    # Convert string dates to datetime.date objects
    start = string_to_date(start_date)
    end = string_to_date(end_date)

    # Validate the conversion and the date range
    if start is None or end is None:
        click.echo(f"Invalid date format. Please provide dates in 'ddmmyyyy' format.")
        return

    if not is_valid_date_range(start, end):
        click.echo(f"Dates must be within the year range [2021, 2022].")
        return

    if start > end:
        click.echo(f"Start date {start_date} is later than end date {end_date}.")
        return

    if process_basic:
        try:
            subprocess.call(['/app/scripts/basic_analytics.sh', start_date, end_date])
            click.echo("Basic analytics pre-processed successfully!")
        except subprocess.CalledProcessError:
            click.echo("An error occurred while processing basic analytics.")

    if process_intermediate:
        click.echo("Intermediate analytics not implemented yet.")

    if process_advanced:
        click.echo("Advanced analytics not implemented yet.")
    
if __name__ == "__main__":
    cli()
