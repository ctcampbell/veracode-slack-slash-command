from helpers.api import VeracodeAPI
from helpers import tools
import get_commands


def process_command(command_type, command_subtype, command_params):
    api = VeracodeAPI()

    if command_type == "get":
        if command_subtype == "apps":
            return get_commands.get_apps(api)
        elif command_subtype == "builds":
            return get_commands.get_builds(api, command_params)
        elif command_subtype == "build":
            return get_commands.get_build(api, command_params)
        else:
            return tools.generate_error(
                "Unknown command `" + " ".join(["/veracode get", command_subtype] + command_params) + "`")
    else:
        # We should have returned by now, so something wasn't recognised or went wrong
        return tools.generate_error(
            "Unknown command `" + " ".join(["/veracode", command_type, command_subtype] + command_params) + "`")
