from os import path
import os
import datetime
import click
from redis_core.redis_core import RedisBaseFunctions


def directory_validator(ctx, param, value):
    if not value:
        raise click.BadParameter("Root directory can not be used for save commits")
    if not path.isdir(f"/home/{os.getlogin()}/{value}"):
        os.mkdir(f"/home/{os.getlogin()}/{value}")
    return f"/home/{os.getlogin()}/{value}"


def file_validator(ctx, param, value: str):
    if value:
        if path.isfile(f"{RedisBaseFunctions.get_work_directory()}/{value}"):
            if value.endswith(".md"):
                return value
        raise click.FileError(value, hint="File does not exist or is not commit file")


def status_validator(ctx, param, value):
    try:
        status = int(value)
        if status > 100 or status < 0:
            raise click.BadParameter(
                "Status value must be integer and in range [0, 100]"
            )
        return status
    except ValueError:
        raise click.BadParameter("Status value must be integer and in range [0, 100]")


def time_option_validator(ctx, param, value):
    try:
        time_value = int(value)
        if time_value > 24 or time_value < 0:
            raise click.BadParameter(
                "Time option value must be integer and in range [0, 24]"
            )
        return time_value
    except ValueError:
        raise click.BadParameter("Status value must be integer and in range [0, 24]")


def date_string_validator(ctx, param, value: str):
    try:
        if value:
            return datetime.datetime.fromisoformat(value)
    except ValueError:
        raise click.BadParameter("Date string must be in isoformat (YYYY-MM-DD)")


def check_directory_without_creating(dir_path):
    if path.isdir(dir_path):
        return True
    raise click.FileError(dir_path, hint="Please, config work directory")
