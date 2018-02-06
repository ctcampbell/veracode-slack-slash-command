import os
import boto3
import json
from urllib.parse import parse_qsl


sub_colour = "#CCCCCC"


def parse_input(data):
    parsed = parse_qsl(data, keep_blank_values=True)
    result = {}
    for item in parsed:
        result[item[0]] = item[1]
    return result


def generate_error(error_text):
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({
            "response_type": "ephemeral",
            "attachments": [
            {
                "fallback": "Error\n" + error_text,
                "title": "Error",
                "text": "```" + error_text + "```",
                "mrkdwn_in": [
                    "text"
                ],
                "color": sub_colour
            }
        ]
        })
    }


def lambda_handler(event, context):
    command_types = ["get", "create", "update", "delete"]

    slack_token = os.environ.get("SLACK_TOKEN", "")
    slack_data = parse_input(event["body"])

    if slack_token == "" or slack_token != slack_data.get("token", ""):
        return generate_error("Error")
    else:
        response = {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": "{}"
        }

        split_text = slack_data["text"].split()
        command_type = split_text[0] if len(split_text) else None

        if command_type in ["help", None]:
            title = "`/veracode` Help"
            text = "To get something, use:\n" + \
                   "```/veracode get apps\n" + \
                   "/veracode get builds <app_id>\n" + \
                   "/veracode get build <build_id>```\n" + \
                   "To get help use: `/veracode help`"
            response["body"] = json.dumps({
                "response_type": "ephemeral",
                "attachments": [
                    {
                        "fallback": title + "\n" + text,
                        "title": title,
                        "text": text,
                        "color": sub_colour
                    }
                ]
            })
            return response

        elif command_type in command_types:
            lambda_client = boto3.client("lambda")
            try:
                lambda_client.invoke(FunctionName="veracodeslackslashcommand",
                                     InvocationType="Event",
                                     Payload=json.dumps(event))
                text = "Talking to Veracode, please hold..."
                response["body"] = json.dumps({
                    "response_type": "in_channel",
                    "attachments": [
                        {
                            "fallback": text,
                            "text": text,
                            "color": sub_colour
                        }
                    ]
                })
            except Exception:
                return generate_error("Error processing `/veracode " + slack_data["text"] + "`")
            return response

        else:
            return generate_error("Unknown command `/veracode " + slack_data["text"] + "`")