import subprocess
import os
import webbrowser
import time
import re
import shutil
import sqlite3
import click
from datetime import date, datetime
import socket
from contextlib import closing

def analytics_files_exist(analytics_type):
    """
    Check if the pre-processed analytics files exist.
    Input can only be 'basic', 'intermediate', 'advanced'
    """
    if analytics_type not in ['basic', 'intermediate', 'advanced']:
        return False
    directory = f'/app/data/analytics/{analytics_type}'
    # Check if the directory exists
    if not os.path.exists(directory):
        return False
    # Check if there are any CSV files in the directory
    return any(fname.endswith('.csv') for fname in os.listdir(directory))

def cleanup_analytics_data(directory):
    """
    Delete the directory if it exists.
    """
    try:
        shutil.rmtree(directory)
        click.echo(f"Cleaned up old analytics data in {directory}.")
    except Exception as e:
        #click.echo(f"An error occurred while cleaning up analytics data: {e}")
        return
        

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

def string_to_date(date_str):
    """
    Convert a string in the format "yyyymmdd" to a datetime.date object.
    """
    try:
        return datetime.strptime(date_str, '%Y%m%d').date()
    except ValueError:
        return None
    
def is_date_arg(arg):
    """"Flag to be used to check if arg can be validly represented as Date"""
    try:
        datetime.strptime(arg, '%Y%m%d').date()
        return True
    except:
        return False

def is_valid_date_range(start_date_str, end_date_str):
    """
    Check if the given start date and end date are within the year range [2021, 2022] and
    start date < end date.
    Return a tuple with the first element being a boolean indicating the date range validity,
    and the second being an error message if applicable.
    """
    min_date = date(2021, 1, 1)
    max_date = date(2022, 12, 31)

    # Check if both dates are in the correct format
    """
    if not is_date_arg(start_date_str):
        return False, f"Error: Invalid date format for start date {start_date_str}"
    
    if not is_date_arg(end_date_str):
        return False, f"Error: Invalid date format for end date {end_date_str}"
    """
    # Convert strings to dates
    start_date = string_to_date(start_date_str)
    end_date = string_to_date(end_date_str)

    # Check if the dates are within the valid range and start date is before the end date
    if not (min_date <= start_date <= max_date):
        return False, f"Error: Start date {start_date_str} is out of the valid range [2021, 2022]"
    
    if not (min_date <= end_date <= max_date):
        return False, f"Error: End date {end_date_str} is out of the valid range [2021, 2022]"
    
    if not (start_date < end_date):
        return False, f"Error: Start date {start_date_str} must be before the end date {end_date_str}"
    
    return True, None  # No errors, dates are valid

def is_flags_arg(arg):
    """"Flag to be used to check if arg represents a flag arg"""
    flag_pattern = re.compile(r'^-(?!.*(.).*\1)[bia]{1,3}$')
    try:
        match = flag_pattern.match(arg)
        if match: 
            return True
        else: 
            return False
    except:
        return False
    
def eval_analytics_flags(flag_arg):
    """
    An evaluation function which will return the different analytics flags extracted from the flag arg.
    Default all flags to true in case flag_arg is None and if the flag arg doesnt match the pattern, return None
    """
    if flag_arg is None:
        # If no flag is provided, set all to True
        return {
            'process_basic': True,
            'process_intermediate': True,
            'process_advanced': True
        }

    # Regular expression to match valid flags with unique characters
    flag_pattern = re.compile(r'^-(?!.*(.).*\1)[bia]{1,3}$')
    match = flag_pattern.match(flag_arg)
    if match:
        # Extract matched groups
        flags = match.group()
        return {
            'process_basic': 'b' in flags,
            'process_intermediate': 'i' in flags,
            'process_advanced': 'a' in flags
        }
    else:
        # If the flag argument doesn't match the pattern, return an error
        return None

def eval_pre_process_analytics_command(args):
    """
    Logic encapsulation regarding all args input by the user 
    to the CLI using pre_process_analytics command
    """
    # Defaults
    default_start_date = '20210101'
    default_end_date = '20221231'
    default_error_message = None
    default_analytics_flags = eval_analytics_flags(None)

     # If no args provided, use default settings (all dates all flags set to True)
    if len(args) == 0:
        return (default_start_date, default_end_date, default_analytics_flags), default_error_message
    # If 1 arg provided, it has to be analytics flag arg (all dates specified flags)
    elif len(args) == 1:
        if not is_flags_arg(args[0]):
            error_message = f"Error: Unknown arg: {args[0]}. If you are to provide only 1 arg, it has to be a valid flag arg e.g. -bi."
            return None, error_message
        else:
            analytics_flags = eval_analytics_flags(args[0])
            return (default_start_date, default_end_date, analytics_flags), default_error_message
    # If 2 args provided, they have to be valid start and end dates(all flags set to True)
    elif len(args) == 2:
        if not is_date_arg(args[0]):
            error_message = f"Error: The provided start_date {args[0]} is not in the correct YYYYMMDD format or the date does not exist."
            return None, error_message
        if not is_date_arg(args[1]):
            error_message = f"Error: The provided end_date {args[1]} is not in the correct YYYYMMDD format or the date does not exist."
            return None, error_message
        valid_date_range, error_message = is_valid_date_range(args[0], args[1])
        if not valid_date_range:
            return None, error_message
        return (args[0], args[1], default_analytics_flags), default_error_message
    # If 3 args provided, they have to be start_date end_date flag arg
    elif len(args) == 3:
        if not is_date_arg(args[0]):
            error_message = f"Error: The provided start_date {args[0]} is not in the correct YYYYMMDD format or the date does not exist."
            return None, error_message
        if not is_date_arg(args[1]):
            error_message = f"Error: The provided end_date {args[1]} is not in the correct YYYYMMDD format or the date does not exist."
            return None, error_message
        valid_date_range, error_message = is_valid_date_range(args[0], args[1])
        if not valid_date_range:
            return None, error_message
        if not is_flags_arg(args[2]):
            error_message = f"Error: The flag arg {args[2]} has to be valid e.g. -bi."
            return None, error_message
        analytics_flags = eval_analytics_flags(args[2])
        return (args[0], args[1], analytics_flags), default_error_message
    # If more than 3 args, error
    else:
        error_message = f"Error: Too many args provided ({len(args)})."
        return None, error_message


def check_port(port):
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        if sock.connect_ex(('localhost', port)) == 0:
            return True # The port is open
        else:
            return False # The port is closed
        
@click.group()
@click.pass_context
def cli(ctx):
    pass

@cli.command()
@click.pass_context  # This decorator ensures that ctx is passed to the function
def repl(ctx):
    """Start a REPL session."""
    def display_initial_commands():
        click.echo("Welcome to the orestiscompany CLI!")
        click.echo("Here are the available commands:")
        click.echo("=========================================")
        click.echo("-----Setup Commands-----:")
        click.echo("  initialize_db                                                 - Initialize the database.")
        click.echo("  populate_db                                                   - Populate the database with data.")
        click.echo("  reset_db                                                      - Reset and repopulate the database.")
        click.echo("  exit or quit                                                  - Exit the CLI.")
        click.echo("")
        click.echo("=========================================")
        click.echo("-----Pre-process Analytics Commands-----")
        click.echo("  pre_process_analytics start_date end_date -arg                - Pre-process analytics for visualizations.")
        click.echo("")
        click.echo("  Note:")
        click.echo("    - dates must be between 20210101 and 20211231, default all dates that data exist [2021, 2022]")
        click.echo("    - arg can be b('basic'), i('intermediate') or a('advanced') analytics, default all")
        click.echo("    - arg can also be bi, ib, ba, ab, ai, ia, as per their combinations")
        click.echo("")
        click.echo("=========================================")
        click.echo("-----Visualization Commands-----")
        click.echo("  visualize_analytics                                           - Visualize all available analytics.")
        click.echo("")
        click.echo("=========================================")
        click.echo("-----Other-----")
        click.echo("  --help                                                        - Re-print this message")
        
    
    # Display the initial commands when the REPL starts 
    display_initial_commands()

    while True:
        command_input = input('orestiscompany> ').strip()
        if not command_input:
            # Skip the loop iteration if the input is empty
            continue

        command_parts = command_input.split()
        base_command = command_parts[0].lower()  # Handle case-insensitive commands
        args = command_parts[1:]

        # Case when user needs help
        if base_command == '--help':
            display_initial_commands()
        # Case when user wants to exit 
        elif base_command == 'exit' or base_command == 'quit':
            break
        # Case when user wants to initialize the database
        elif base_command == 'initialize_db':
            ctx.invoke(initialize_db)
        # Case when the user wants to populate the database
        elif base_command == 'populate_db':
            ctx.invoke(populate_db)
        # Case when the user wants to reset the database
        elif base_command == 'reset_db':
            ctx.invoke(reset_db)
        # Case when the user wants to pre process the analytics
        elif base_command == 'pre_process_analytics':
            evaluated_command, error = eval_pre_process_analytics_command(args)
            if error:
                # Report the error and skip the rest of the loop and prompt the user for a new command
                click.echo(error)
                continue  
            else:
                new_start_date, new_end_date, analytics_flags = evaluated_command
                if analytics_flags is not None:
                    ctx.invoke(pre_process_analytics, 
                               start_date=new_start_date, 
                               end_date=new_end_date, 
                               **analytics_flags)
        # Case when the user wants to visualize the analytics
        elif base_command == 'visualize_analytics':
            ctx.invoke(visualize_analytics)
        else:
            click.echo(f"Unknown command: {base_command}")
            # Optionally, you can offer to show the help again
            if click.confirm("Would you like to see the help instructions again?"):
                display_initial_commands()


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
     # Clean up existing analytics data
    cleanup_analytics_data("/app/data/analytics")

    # Check if the database is initialized and populated
    if not db_initialized():
        click.echo("It seems the database hasn't been initialized yet. Please initialize_db first.")
        return
    if not db_populated():
        click.echo("It seems the database hasn't been populated yet. Please populate_db first.")
        return
    
    # Convert string dates to datetime.date objects
    #start = string_to_date(start_date)
    #end = string_to_date(end_date)

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
def visualize_analytics(ctx):
    """Visualize analytics."""
    # Check if the database is initialized and populated
    if not db_initialized():
        click.echo("It seems the database hasn't been initialized yet.")
        if click.confirm("Would you like to initialize the db now?", default=True):
            ctx.invoke(initialize_db)
        else:
            click.echo("Please initialize_db  before visualizing analytics.")
        return
    if not db_populated():
        click.echo("It seems the database hasn't been populated yet.")
        if click.confirm("Would you like to populate the db now?", default=True):
            ctx.invoke(populate_db)
        else:
            click.echo("Please populate_db before visualizing analytics.")
        return
        
    # Check what analytics files exist
    basic_analytics_exists, intermediate_analytics_exists, advanced_analytics_exist = \
        (analytics_files_exist(level) for level in ['basic', 'intermediate', 'advanced'])
    
    if not any((basic_analytics_exists, intermediate_analytics_exists, advanced_analytics_exist)):
        click.echo("It seems there are no pre processed analytics available to visualize")
        click.echo("Please check the pre_process_analytics command")

    PORT = 8050
    if analytics_files_exist('basic'):
        if check_port(PORT):
            click.echo(f"Dash visualization server is already running on port {PORT}, check http://localhost:8050")
            click.echo(f"You can even do reset_db and pre_process_analytics again and the visualization server will adjust")
        else:
            try:
                # Execute the basic_analytics_viz.sh script (this will start the Dash(Flask) Server)
                # Completely disregard any stdout/stderr and dont keep logs, 
                # When user exits the CLI then the Dash server will get SIGKILLL anyways.
                # All of the above are outside this project's scope.
                subprocess.Popen(
                    ["/app/scripts/analytics_viz.sh"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                    )
                
                
                # Wait a couple of seconds for the server to start
                time.sleep(2)
                click.echo("Visualization for basic analytics should now be in 'http://localhost:8050/'")
            except Exception as e:
                click.echo(f"An error occurred while visualizing basic analytics: {e}")

    return



if __name__ == "__main__":
    cli()
