import pytz
from datetime import datetime
from helpers import tools
from helpers.api import VeracodeAPIError


vc_colour = "#D73185"


def get_apps(api):
    try:
        apps = tools.parse_xml(api.get_app_list()).findall("app")
    except VeracodeAPIError:
        return tools.generate_error("Unable to list apps")

    title = "Veracode app list"
    message = ""
    for app in apps:
        policy_updated_date_utc = datetime.strptime(app.attrib["policy_updated_date"][:22]
                                                    + app.attrib["policy_updated_date"][23:],
                                                    "%Y-%m-%dT%H:%M:%S%z").astimezone(pytz.utc)
        message += "*" + app.attrib["app_name"] + "*\n" + \
                   "```App ID: " + app.attrib["app_id"] + "\n" + \
                   "Last updated: " + policy_updated_date_utc.strftime("%Y-%m-%d %H:%M:%S %Z") + "```\n"
    simple_message = title + "\n" + message

    return {
        "response_type": "in_channel",
        "attachments": [
            {
                "fallback": simple_message,
                "title": title,
                "text": message,
                "mrkdwn_in": [
                    "text",
                    "fallback"
                ],
                "color": vc_colour,
            }
        ],
    }


def get_builds(api, command_params):
    if not command_params:
        return tools.generate_error("App ID missing in `/veracode get builds`")
    elif len(command_params) == 1 and command_params[0].isdigit():
        try:
            build_list = tools.parse_xml(api.get_build_list(command_params[0]))
            builds = reversed(build_list.findall("build")[-10:])
        except VeracodeAPIError:
            return tools.generate_error("Unable to list builds")

        title = build_list.attrib["app_name"] + " build list (last 10)"
        message = ""
        for build in builds:
            policy_updated_date_utc = datetime.strptime(build.attrib["policy_updated_date"][:22]
                                                        + build.attrib["policy_updated_date"][23:],
                                                        "%Y-%m-%dT%H:%M:%S%z").astimezone(pytz.utc)
            message += "*" + build.attrib["version"] + "*\n" + \
                       "```Build ID: " + build.attrib["build_id"] + "\n" + \
                       "Last updated: " + policy_updated_date_utc.strftime("%Y-%m-%d %H:%M:%S %Z") + "```\n"
        simple_message = title + "\n" + message

        return {
            "response_type": "in_channel",
            "attachments": [
                {
                    "fallback": simple_message,
                    "title": title,
                    "text": message,
                    "mrkdwn_in": [
                        "text",
                        "fallback"
                    ],
                    "color": vc_colour,
                }
            ],
        }
    else:
        return tools.generate_error("App ID error in `" + " ".join(["/veracode get builds"] + command_params) + "`")


def get_build(api, command_params):
    if not command_params:
        return tools.generate_error("Build ID missing in `/veracode get build`")
    elif len(command_params) == 1 and command_params[0].isdigit():
        try:
            detailed_report = tools.parse_xml(api.get_detailed_report(command_params))
            build_info = tools.parse_xml(api.get_build_info(detailed_report.attrib["app_id"], command_params[0]))
        except VeracodeAPIError:
            return tools.generate_error("Unable to get build " + command_params[0])

        link = "https://analysiscenter.veracode.com/auth/index.jsp#ViewReportsDetailedReport:" + \
               ":".join([build_info.attrib["account_id"],
                         build_info.attrib["app_id"],
                         build_info.attrib["build_id"]])

        title = detailed_report.attrib["version"]
        message = "```Build ID: " + detailed_report.attrib["build_id"] + \
                  "\nLast updated: " + detailed_report.attrib["last_update_time"] + \
                  "\nTotal flaws: " + detailed_report.attrib["total_flaws"] + \
                  "\nPolicy compliance: " + detailed_report.attrib["policy_compliance_status"] + "```"
        simple_message = title + "\n" + message + "\nReport link: " + link

        return {
            "response_type": "in_channel",
            "attachments": [
                {
                    "fallback": simple_message,
                    "title": title,
                    "text": message,
                    "mrkdwn_in": [
                        "text",
                        "fallback"
                    ],
                    "color": vc_colour,
                    "actions": [
                        {
                            "type": "button",
                            "text": "Open Report",
                            "url": link
                        }
                    ]
                }
            ],
        }
    else:
        return tools.generate_error("Build ID error in `" + " ".join(["/veracode get build"] + command_params) + "`")
