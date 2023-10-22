import click
import subprocess

@click.group()
def cli():
    pass

@cli.command()
def reset_db():
    """Reset and repopulate the database."""
    confirmation = click.confirm("Are you sure you want to reset and repopulate the database? This action is irreversible.", abort=True)
    if confirmation:
        try:
            # Execute the reset_db.sh script
            subprocess.run(["/app/reset_db.sh"], check=True)
            click.echo("Database reset and repopulated successfully!")
        except subprocess.CalledProcessError:
            click.echo("An error occurred while resetting the database.")

if __name__ == "__main__":
    cli()
