import hashlib
import os

from redis import Redis
from redis_core.redis_data import REDIS_DATA, UserStructure, VKPM_NICKNAME


class RedisBaseFunctions:
    connect = Redis(**REDIS_DATA, decode_responses=True)

    @classmethod
    def config_data(cls, username, password, work_directory):
        data = {
            UserStructure.email: username,
            UserStructure.password: hashlib.md5(password.encode("utf-8")).hexdigest(),
            UserStructure.work_directory: work_directory,
            UserStructure.default_project: "",
            UserStructure.default_activity: "",
            UserStructure.default_status: "",
        }
        for i in data.keys():
            cls.connect.hset(VKPM_NICKNAME, i, data[i])

    @classmethod
    def change_work_directory(cls, new_work_directory):
        cls.connect.hset(
            VKPM_NICKNAME, UserStructure.work_directory, new_work_directory
        )

    @classmethod
    def change_default_project(cls, new_default_project):
        cls.connect.hset(
            VKPM_NICKNAME, UserStructure.default_project, new_default_project
        )

    @classmethod
    def change_default_activity(cls, new_default_activity):
        cls.connect.hset(
            VKPM_NICKNAME, UserStructure.default_activity, new_default_activity
        )

    @classmethod
    def change_default_status(cls, new_default_status):
        cls.connect.hset(
            VKPM_NICKNAME, UserStructure.default_status, new_default_status
        )

    @classmethod
    def get_status(cls):
        return cls.connect.hget(VKPM_NICKNAME, UserStructure.default_status)

    @classmethod
    def get_work_directory(cls):
        return cls.connect.hget(VKPM_NICKNAME, UserStructure.work_directory)

    @classmethod
    def get_default_project(cls):
        return cls.connect.hget(VKPM_NICKNAME, UserStructure.default_project)

    @classmethod
    def get_default_activity(cls):
        return cls.connect.hget(VKPM_NICKNAME, UserStructure.default_activity)

    @classmethod
    def check_login_and_password(cls, login, password):
        saved_login = cls.connect.hget(VKPM_NICKNAME, UserStructure.email)
        saved_password = cls.connect.hget(VKPM_NICKNAME, UserStructure.password)
        hash_pass = hashlib.md5(password.encode("utf-8")).hexdigest()
        if login != saved_login or saved_password != hash_pass:
            return False
        return True

    @classmethod
    def change_user(cls, login, password):
        cls.config_data(login, password, cls.get_work_directory())
