import os
import json
import commands
import requests
from urllib.parse import parse_qsl
from helpers import tools


def parse_input(data):
    parsed = parse_qsl(data, keep_blank_values=True)
    result = {}
    for item in parsed:
        result[item[0]] = item[1]
    return result


def main(event, context):
    slack_token = os.environ.get("SLACK_TOKEN", "")
    slack_data = parse_input(event["body"])
    command_types = ["get", "create", "update", "delete"]
    command_subtypes = ["app", "sandbox", "build", "policy", "user", "apps", "sandboxes", "builds", "policies", "users"]

    # Check Slack token matches
    if slack_token == "" or slack_token != slack_data.get("token", ""):
        return
    else:
        split_text = slack_data["text"].split()
        if len(split_text) >= 2:
            command_type = split_text.pop(0)
            command_subtype = split_text.pop(0)
            if command_type in command_types and command_subtype in command_subtypes:
                command_output = commands.process_command(command_type, command_subtype, split_text)
                requests.post(slack_data["response_url"], data=json.dumps(command_output))
                return command_output
            else:
                error = tools.generate_error("Unknown command in `/veracode " + slack_data["text"] + "`")
                requests.post(slack_data["response_url"], data=json.dumps(error))
                return error
        else:
            error = tools.generate_error("Missing command in `" + " ".join(["/veracode", slack_data["text"]]) + "`")
            requests.post(slack_data["response_url"], data=json.dumps(error))
            return error


def lambda_handler(event, context):
    return main(event, context)
