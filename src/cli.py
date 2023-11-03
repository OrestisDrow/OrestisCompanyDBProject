import subprocess
import sqlite3
import click
from datetime import date, datetime
import os
import webbrowser
import time
import re

def string_to_date(date_str):
    """
    Convert a string in the format "yyyymmdd" to a datetime.date object.
    """
    try:
        return datetime.strptime(date_str, '%Y%m%d').date()
    except ValueError:
        return None
    
def is_valid_date_range(start_date_str, end_date_str):
    """
    Check if the given start_date and end_date are within the year range [2021, 2022].
    """
    start_date = datetime.strptime(start_date_str, "%Y%m%d").date()
    end_date = datetime.strptime(end_date_str, "%Y%m%d").date()
    
    min_date = date(2021, 1, 1)
    max_date = date(2022, 12, 31)
    
    return min_date <= start_date <= max_date and min_date <= end_date <= max_date and start_date <= end_date


def basic_analytics_files_exist():
    """Check if the pre-processed basic analytics files exist."""
    directory = '/app/data/analytics/basic'
    # Check if the directory exists
    if not os.path.exists(directory):
        return False
    # Check if there are any CSV files in the directory
    return any(fname.endswith('.csv') for fname in os.listdir(directory))


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
    click.echo("")
    click.echo("  Note:")
    click.echo("    - dates must be between 20210101 and 20211231, default all dates that data exist [2021, 2022]")
    click.echo("    - arg can be b('basic'), i('intermediate') or a('advanced') analytics, default all")
    click.echo("    - arg can also be bi, ib, ba, ab, ai, ia, as per their combinations")
    click.echo("")
    click.echo("-----Visualization Commands-----")
    click.echo("(in progress)")
    click.echo("  visualize_basic_analytics         - Visualize basic analytics.")
    click.echo("  visualize_intermediate_analytics  - Visualize intermediate analytics.")
    click.echo("  visualize_advanced_analytics      - Visualize advanced analytics.")
    click.echo("")
    
    date_pattern = re.compile(r'^\d{4}\d{2}\d{2}$')
    
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

            if len(args) > 0:
                if date_pattern.match(args[0]):
                    start_date = args[0]
                else:
                    print(f"Error: The provided start_date {args[0]} is not in the correct YYYYMMDD format.")
                    continue  # Skip the rest of the loop and prompt the user for a new command

            if len(args) > 1:
                if date_pattern.match(args[1]):
                    end_date = args[1]
                else:
                    print(f"Error: The provided end_date {args[1]} is not in the correct YYYYMMDD format.")
                    continue

            if not is_valid_date_range(args[0], args[1]):
                print(f"Error: The provided start and end dates: [{args[0]},{args[1]}] are not within the year range [2021, 2022] or start > end date.")
                continue

            ctx.invoke(pre_process_analytics, start_date=start_date, end_date=end_date, process_basic=process_basic, process_intermediate=process_intermediate, process_advanced=process_advanced)
        elif base_command == 'visualize_basic_analytics':
            ctx.invoke(visualize_basic_analytics)
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

    if process_basic:
        try:
            subprocess.call(['/app/scripts/basic_analytics.sh', start_date, end_date])
            click.echo("Basic analytics pre-processed successfully!")
        except subprocess.CalledProcessError:
            click.echo("An error occurred while processing basic analytics.")

    if process_intermediate:
        try:
            subprocess.call(['/app/scripts/intermediate_analytics.sh', start_date, end_date])
            click.echo("Intermediate analytics pre-processed successfully!")
        except subprocess.CalledProcessError:
            click.echo("An error occurred while processing intermediate analytics.")

    if process_advanced:
        click.echo("Advanced analytics not implemented yet.")
    
@cli.command()
@click.pass_context
def visualize_basic_analytics(ctx):
    """Visualize basic analytics."""
    # Check if the database is initialized and populated
    if not db_initialized():
        click.echo("The database hasn't been initialized. Please initialize it before pre-processing analytics.")
        return
    if not db_populated():
        click.echo("The database hasn't been populated. Please populate it before pre-processing analytics.")
        return
    
    # Check if the basic analytics files exist
    if not basic_analytics_files_exist():
        click.echo("It seems the basic analytics data hasn't been pre-processed yet.")
        if click.confirm("Would you like to pre-process it now with the default settings?", default=True):
            # Invoke pre_process_analytics with default settings
            ctx.invoke(pre_process_analytics, start_date='20210101', end_date='20221231', process_basic=True, process_intermediate=False, process_advanced=False)
        else:
            click.echo("Please pre-process the basic analytics data before visualizing.")
            return

    try:
        # Execute the basic_analytics_viz.sh script (thhis will start the Dash/Flask Server)
        subprocess.run(["/app/scripts/basic_analytics_viz.sh"], check=True)
        # Wait a couple of seconds for the server to start
        time.sleep(2)
        # Open the user's default browser or a new tab if it's already open
        # webbrowser.open_new_tab('http://localhost:8050/')
        click.echo("Visualization for basic analytics should now be in 'http://localhost:8050/'")
    except subprocess.CalledProcessError:
        click.echo("An error occurred while visualizing basic analytics.")



if __name__ == "__main__":
    cli()
