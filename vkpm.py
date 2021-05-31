import click
from datetime import date, datetime
from redis_core.redis_core import RedisBaseFunctions
from commit.commit import Commit
from utils import validators, file_utils


@click.group()
def cli():
    pass


@cli.command()
@click.option("-u", "--username", prompt=True)
@click.password_option(
    "-p", "--password", prompt=True, hide_input=True, confirmation_prompt=True
)
def login(username, password):
    """
    Using for loging user into "vkpm" system (заглушка)
    """
    if RedisBaseFunctions.check_login_and_password(username, password):
        click.echo(f"Welcome, {username}")
        return
    click.echo("Error, something is incorrect")



@cli.command()
@click.option("-u", "--username", prompt=True)
@click.password_option(prompt=True)
@click.option(
    "-w",
    "--work_directory",
    callback=validators.directory_validator,
    type=click.Path(),
    prompt=True,
)
def config(username, password, work_directory):
    """
    Using for config user into local system
    """
    RedisBaseFunctions.config_data(username, password, work_directory)


@cli.command()
@click.option("-f", "--force", is_flag=True)
def pull(force):
    """
    Using for pull user info from "vkpm" system (заглушка)
    """
    if force:
        click.echo("force pull")
        return
    click.echo("base pull")


@cli.command()
@click.option("-u", "--username", prompt=True)
@click.password_option(
    "-p", "--password", prompt=True, hide_input=True, confirmation_prompt=True
)
def push(username, password):
    """
    Using for push user data into "vkpm" system (заглушка)
    """
    if RedisBaseFunctions.check_login_and_password(username, password):
        click.echo('allow')
    else:
        click.echo('anathema')


@cli.command()
@click.argument(
    "work_directory", callback=validators.directory_validator, type=click.Path()
)
def change_wd(work_directory):
    """
    Using for change user work directory into local system
    """
    file_utils.move_files(RedisBaseFunctions.get_work_directory(), work_directory)
    RedisBaseFunctions.change_work_directory(work_directory)
    click.echo(RedisBaseFunctions.get_work_directory())


@cli.command()
@click.argument("name", callback=validators.file_validator)
def delete(name):
    """
    Delete commit by name
    """
    Commit().delete(RedisBaseFunctions.get_work_directory(), name)
    click.echo(f"delete commit {name}")


@cli.command()
@click.option("-a", "--all", "all_names", is_flag=True)
@click.option("-n", "--name", callback=validators.file_validator)
def read(all_names, name):
    """
    Read commit by name or all commits names
    """
    validators.check_directory_without_creating(RedisBaseFunctions.get_work_directory())
    if all_names and name:
        click.echo("choice only one option")
    elif all_names:
        click.echo(f"show all commits")
        Commit().read_names(RedisBaseFunctions.get_work_directory())
    elif name:
        click.echo(f"show commit {name}")
        click.echo(Commit().read(RedisBaseFunctions.get_work_directory(), name))
    elif not all_names and not name:
        commit_name = click.prompt("Enter the commit name: ")
        click.echo(f"show commit {commit_name}")
        click.echo(Commit().read(RedisBaseFunctions.get_work_directory(), commit_name))


@cli.command()
@click.option("--project", type=str, default=None)
@click.option("-o", "--overtime", is_flag=True, default=None)
@click.option("-n", "--task_name", prompt=True)
@click.option("-d", "--description", prompt=True)
@click.option("-p", "--task_status", prompt=True, callback=validators.status_validator)
@click.option("--report_date", type=str, callback=validators.date_string_validator)
@click.option(
    "-t",
    "--time_interval",
    type=int,
    callback=validators.time_option_validator,
    default=0,
)
@click.option(
    "-s", "--start", type=int, callback=validators.time_option_validator, default=0
)
@click.option(
    "-f", "--finish", type=int, callback=validators.time_option_validator, default=0
)
@click.option(
    "--activity",
    type=click.Choice(
        ["Estimate", "Development", "Testing", "Bugfixing", "Management", "Analysis"],
        case_sensitive=False,
    ),
    default="Development",
)
def commit(
    project: str,
    overtime: bool,
    task_status,
    task_name: str,
    description: str,
    report_date: str,
    time_interval: int,
    start: int,
    finish: int,
    activity: str,
):
    """
    Create commit and write it into file
    """
    data = {
        "task_name": task_name,
        "task_description": description,
        "activity": activity,
        "task_status": task_status,
    }
    RedisBaseFunctions.change_default_activity(activity)
    if project:
        data["project"] = project
        RedisBaseFunctions.change_default_project(project)
    else:
        saved_project = RedisBaseFunctions.get_default_project()
        if not saved_project:
            saved_project = click.prompt("Enter the project name")
        data["project"] = saved_project
        RedisBaseFunctions.change_default_project(saved_project)
    if not report_date:
        data["report_date"] = date.today().isoformat()
    else:
        data["report_date"] = report_date
    if task_status:
        data["task_status"] = task_status
    if overtime:
        data["overtime"] = True
    else:
        data["overtime"] = False
    if time_interval and (start or finish):
        click.echo(
            "Error, use time interval(-t) without start(-s) or finish(-f) options"
        )
        return
    elif time_interval:
        data["start_time"] = datetime.now().hour - time_interval
        data["end_time"] = datetime.now().hour
    else:
        if not start:
            data["start_time"] = click.prompt("Enter start hour")
        else:
            data["start_time"] = start
        if not finish:
            data["end_time"] = click.prompt("Enter finish hour")
        else:
            data["end_time"] = finish
    if data["start_time"] > data["end_time"]:
        raise click.BadParameter("Start time can not be later that finish time")
    Commit().write_into_file(
        RedisBaseFunctions.get_work_directory(), str(datetime.now()), **data
    )


@cli.command()
@click.argument("commit_name", callback=validators.file_validator)
@click.option("--project", type=str)
@click.option("-o", "--overtime", is_flag=True)
@click.option("-p", "--task_status", callback=validators.status_validator)
@click.option("-n", "--task_name", type=str)
@click.option("-d", "--description", type=str)
@click.option("--report_date", type=str, callback=validators.date_string_validator)
@click.option(
    "-t",
    "--time_interval",
    type=int,
    callback=validators.time_option_validator,
    default=0,
)
@click.option(
    "-s", "--start_time", type=int, callback=validators.time_option_validator, default=0
)
@click.option(
    "-f", "--end_time", type=int, callback=validators.time_option_validator, default=0
)
@click.option(
    "--activity",
    type=click.Choice(
        ["Estimate", "Development", "Testing", "Bugfixing", "Management", "Analysis"],
        case_sensitive=False,
    ),
)
def edit(commit_name, **kwargs):
    """
    Edit commit by commit name
    """
    Commit().update(RedisBaseFunctions.get_work_directory(), commit_name, kwargs)
