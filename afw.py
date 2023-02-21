#!/usr/bin/env python

import json
import subprocess
from pathlib import Path
from uuid import uuid4
from zipfile import ZipFile

import click

FILENAME_LIST = (
    "info.plist",
    "entry_point.py",
    "core.py",
)

PATH_LIST = (
    "arrow",
    "backports",
    "dateutil",
    "ualfred",
)


# def main():
#     with open("version") as f:
#         version = f.readline().rstrip("\n\r ")
#
#     zip_filename = f"time-converter.{version}.alfredworkflow"
#     z = ZipFile(zip_filename, mode="w")
#
#     for filename in FILENAME_LIST:
#         z.write(filename)
#
#     for pathname in PATH_LIST:
#         for root, dirs, files in walk(pathname):
#             for filename in files:
#                 if filename.rfind(".pyc") == -1:
#                     z.write(join(root, filename))
#
#     z.close()
#
#     print(f"Create Alfred workflow({zip_filename}) finished.")


@click.group()
def cli():
    pass


@cli.command()
@click.argument("workflow_path")
def build(workflow_path: str):
    workflow_path = Path(".").joinpath(workflow_path)

    # load package info
    with open(workflow_path.joinpath("package.json")) as f:
        package_info = json.load(f)

    # build package
    build_path = Path(".").joinpath("build").joinpath(uuid4().hex)
    build_path.mkdir(parents=True)
    dist_path = Path(".").joinpath("dist")
    dist_path.mkdir(exist_ok=True)
    package_path = dist_path.joinpath(
        f"{package_info['name']}.{package_info['version']}.alfredworkflow"
    )

    # build package - depend
    print("Prepare...")
    requirements: list[str] = list()
    with open(workflow_path.joinpath("requirements.txt")) as f:
        for line in f.readlines():
            if line.startswith("#") or len(line) == 0:
                continue

            requirements.append(line)

    for requirement in requirements:
        subprocess.run(
            ["pip", "install", "-U", f"--target={str(build_path)}", requirement],
            capture_output=True,
        )

    # build package - zip
    package_file = ZipFile(package_path, mode="w")

    # for filename in FILENAME_LIST:
    #     package_file.write(filename)

    print("Add 3rd depends files...")
    build_path_str_length = len(str(build_path)) + 1
    for file in build_path.rglob("*"):
        if file.suffix == ".pyc" or file.name == "__pycache__":
            continue

        arc_name = str(file)[build_path_str_length:]
        print(arc_name)
        package_file.write(file, arcname=arc_name)

    print("Add workflow files...")
    workflow_files: list[str] = ["info.plist", "main.py", "__init__.py"]
    icon_file = package_info.get("icon")
    if icon_file:
        workflow_files.append(icon_file)

    for file in workflow_files:
        package_file.write(workflow_path.joinpath(file), arcname=file)

    package_file.write("entry_point.py")

    package_file.close()
    print(f"Create Alfred workflow[{package_path}] finished.")


@cli.command()
def test():
    click.echo("test...todo")


if __name__ == "__main__":
    cli()
