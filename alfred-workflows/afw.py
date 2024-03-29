#!/usr/bin/env python

import importlib
import json
import logging
import subprocess
import sys
from pathlib import Path
from uuid import uuid4
from zipfile import ZipFile

import click
from ualfred import Workflow3

AFW_RUNTIME_FILES = ["afw.py", "afw_runtime.py"]
AFW_REQUIREMENTS = ["click", "ualfred"]

AFW_WORKFLOW_BASIC_FILES = ["info.plist", "main.py"]


@click.group()
def cli():
    pass


@cli.command()
@click.argument("workflow_path")
def build(workflow_path: str):
    logging.basicConfig(level=logging.INFO)

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
    logging.info("Prepare...")
    requirements: list[str] = list()
    with open(workflow_path.joinpath("requirements.txt")) as f:
        for line in f.readlines():
            if line.startswith("#") or len(line) == 0:
                continue

            requirements.append(line)

    requirements += AFW_REQUIREMENTS
    for requirement in requirements:
        subprocess.run(
            ["pip", "install", "-U", f"--target={str(build_path)}", requirement],
            capture_output=True,
        )

    # build package - zip
    package_file = ZipFile(package_path, mode="w")

    # for filename in FILENAME_LIST:
    #     package_file.write(filename)

    logging.info("Add 3rd depends files...")
    build_path_str_length = len(str(build_path)) + 1
    for file in build_path.rglob("*"):
        if file.suffix == ".pyc" or file.name == "__pycache__":
            continue

        arc_name = str(file)[build_path_str_length:]
        logging.info(arc_name)
        package_file.write(file, arcname=arc_name)

    logging.info("Add workflow files...")
    workflow_files: list[str] = AFW_WORKFLOW_BASIC_FILES
    icon_file = package_info.get("icon")
    if icon_file:
        workflow_files.append(icon_file)

    for file in workflow_files:
        package_file.write(workflow_path.joinpath(file), arcname=file)

    for file in AFW_RUNTIME_FILES:
        package_file.write(file)

    package_file.close()

    logging.info(f"Create Alfred workflow[{package_path}] finished.")


def afw_entry(workflow):
    # The Workflow3 instance will be passed to the function
    # you call from `Workflow3.run`.
    # Not super useful, as the `wf` object created in
    # the `if __name__ ...` clause below is global...
    #
    # Your imports go here if you want to catch import errors, which
    # is not a bad idea, or if the modules/packages are in a directory
    # added via `Workflow3(libraries=...)`
    # import somemodule
    # import anothermodule

    # Get args from Workflow3, already in normalized Unicode.
    # This is also necessary for "magic" arguments to work.
    # args = wf.args

    args = workflow.args[1:]

    # Do stuff here ...
    from main import main as afw_workflow_main

    feedback = afw_workflow_main(args, workflow.logger)

    # Add an item to Alfred feedback
    # wf.add_item(u'Item title', u'Item subtitle')
    for item in feedback:
        workflow.add_item(**item)

    # Send output to Alfred. You can only call this once.
    # Well, you *can* call it multiple times, but subsequent calls
    # are ignored (otherwise the JSON sent to Alfred would be invalid).
    workflow.send_feedback()


@cli.command()
@click.argument("query", default="")
def call(query):
    # Create a global `Workflow3` object
    wf = Workflow3()
    # Call your entry function via `Workflow3.run()` to enable its
    # helper functions, like exception catching, ARGV normalization,
    # magic arguments etc.
    sys.exit(wf.run(afw_entry))


@cli.command()
@click.argument("workflow_path")
@click.argument("query", default="")
def test(workflow_path: str, query: str):
    try:
        module = importlib.import_module(workflow_path, "main")
    except ImportError as e:
        print(e)
        exit(1)

    wf = Workflow3()

    logging.basicConfig(level=logging.DEBUG)
    feedback = module.main(args=wf.args[2:], logger=logging)
    print(json.dumps(feedback, indent=4))


if __name__ == "__main__":
    cli()
