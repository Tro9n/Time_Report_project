from commit.commit_structure import COMMIT_STRUCTURE
import click
from os import path, listdir, remove, getlogin


class Commit:
    @staticmethod
    def write_into_file(
        directory,
        commit_name,
        project,
        report_date,
        activity,
        task_status,
        start_time,
        end_time,
        overtime,
        task_name,
        task_description,
    ):
        with click.open_file(f"{directory}/{commit_name}.md", "w") as commit_file:
            commit_file.write(
                COMMIT_STRUCTURE.format(
                    commit_name=commit_name,
                    project=project,
                    report_date=report_date,
                    activity=activity,
                    task_status=task_status,
                    start_time=start_time,
                    end_time=end_time,
                    overtime=overtime,
                    task_name=task_name,
                    description=task_description,
                )
            )

    @staticmethod
    def delete(directory, commit_name):
        if path.exists(f"{directory}/{commit_name}"):
            remove(f"{directory}/{commit_name}")
            return True
        return False

    @staticmethod
    def read(directory, commit_name):
        if path.exists(f"{directory}/{commit_name}"):
            with open(f"{directory}/{commit_name}", "r") as commit_file:
                commit_text = commit_file.read()
            return commit_text
        return False

    @staticmethod
    def read_names(directory):
        md_files = [
            f
            for f in listdir(directory)
            if path.isfile(path.join(directory, f)) and f.endswith(".md")
        ]
        for i in md_files:
            click.echo(i)

    @staticmethod
    def parse_commit(commit_text):
        if commit_text:
            return commit_text.split("\n")

    def update(self, directory, commit_name, data: dict):
        parsed_commit = self.parse_commit(self.read(directory, commit_name))
        parsed_structure = self.parse_commit(COMMIT_STRUCTURE)
        update_list = []
        for structure in parsed_structure:
            change = ""
            for option in data.keys():
                if data[option]:
                    if option in structure:
                        change = structure.replace(
                            "{" + option + "}", str(data[option])
                        )
                        break
            if change:
                update_list.append(change)
                continue
        for count in range(len(parsed_commit)):
            for update in update_list:
                if parsed_commit[count].startswith(update[: update.find("|")]):
                    parsed_commit[count] = update
        updated_commit = "\n".join(parsed_commit)
        with click.open_file(f"{directory}/{commit_name}", "w") as commit_file:
            commit_file.write(updated_commit)
