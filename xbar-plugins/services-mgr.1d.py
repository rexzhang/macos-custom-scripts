#!/usr/bin/env python3
# Metadata allows your plugin to show up in the app, and website.
#
#  <xbar.title>Services Mgr</xbar.title>
#  <xbar.version>v1.0</xbar.version>
#  <xbar.author>Rex Zhang</xbar.author>
#  <xbar.author.github>rexzhang</xbar.author.github>
#  <xbar.desc>Configuration-driven service start/stop tool.</xbar.desc>
#  <xbar.image>http://www.hosted-somewhere/pluginimage</xbar.image>
#  <xbar.dependencies>python3.11+</xbar.dependencies>
#  <xbar.abouturl>https://github.com/rexzhang/xbar-plugins</xbar.abouturl>


import re
import subprocess
import tomllib
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path

SUDO_EXECUTABLE = "/usr/bin/sudo"
CONFIG_FILE_NAME = "services-mgr.toml"
CONFIG_FILE_PATHS = [
    Path(__file__).parent,
    Path.home(),
    Path.home().joinpath(".config"),
]
MENU_FORMAT_START_SERVICE = "-- Start | shell={} | terminal=False | refresh=True"
MENU_FORMAT_STOP_SERVICE = "-- Stop | shell={} | terminal=False | refresh=True"


class ServiceStatus(Enum):
    UNKNOW = "UNKNOW"
    ON = "ON"
    OFF = "OFF"
    ERROR = "ERROR"


@dataclass
class Service:
    name: str
    start_shell: list[str]
    stop_shell: list[str]

    status: ServiceStatus = field(default=ServiceStatus.UNKNOW)
    status_shell: list[str] = field(default_factory=list)
    status_on_regex: str = field(default_factory=str)


def load_config() -> list[Service]:
    data = None
    for cf_path in CONFIG_FILE_PATHS:
        cf_filename = cf_path.joinpath(CONFIG_FILE_NAME)
        try:
            with open(cf_filename, "rb") as f:
                try:
                    data = tomllib.load(f)
                except tomllib.TOMLDecodeError:
                    data = []

                break

        except FileNotFoundError:
            pass

    if data is None:
        print(f"Can't found configuration file <{CONFIG_FILE_NAME}>")
        exit()

    if "services" not in data:
        print(f"Configuration file format error <{cf_filename}>")
        exit()

    services = list()
    for item in data["services"]:
        # TODO: do something, check it...
        try:
            services.append(Service(**item))
        except TypeError as e:
            raise TypeError(f"item:{str(item)}. {e}")

    return services


def get_services_status(services: list[Service]) -> list[Service]:
    for index in range(len(services)):
        service = services[index]
        if len(service.status_shell) == 0 or len(service.status_on_regex) == 0:
            continue

        result = subprocess.run(service.status_shell, capture_output=True)
        m = re.search(service.status_on_regex, result.stdout.decode("utf-8"))
        if m is None:
            services[index].status = ServiceStatus.OFF
        else:
            services[index].status = ServiceStatus.ON

    return services


def _convert_shell_call_to_menu_str(shell_call: list[str]) -> str:
    if len(shell_call) == 0:
        return ""

    result = f"'{shell_call[0]}'"
    for index in range(1, len(shell_call)):
        result += f" param{index}='{shell_call[index]}'"

    return result


def print_menu(services: list[Service]):
    print("Smgr")
    print("---")

    for service in services:
        if service.status == ServiceStatus.UNKNOW:
            print(f"{service.name}")
        else:
            print(f"{service.name}: {service.status.name}")

        if service.status == ServiceStatus.ON:
            print("-- Start")
        else:
            print(
                MENU_FORMAT_START_SERVICE.format(
                    _convert_shell_call_to_menu_str(service.start_shell)
                )
            )

        if service.status == ServiceStatus.OFF:
            print("-- Stop")
        else:
            print(
                MENU_FORMAT_STOP_SERVICE.format(
                    _convert_shell_call_to_menu_str(service.stop_shell)
                )
            )

    print("---")
    print("Refresh | refresh=true")


def main():
    services = load_config()
    services = get_services_status(services)
    print_menu(services)


if __name__ == "__main__":
    main()
