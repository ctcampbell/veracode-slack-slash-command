import xml.etree.ElementTree as ETree
from io import BytesIO


def parse_xml(xml_string):
    it = ETree.iterparse(BytesIO(xml_string))
    for _, el in it:
        if "}" in el.tag:
            el.tag = el.tag.split("}", 1)[1]  # strip all namespaces
    return it.root


def diff(first, second, comparator):
    second = set(item.attrib[comparator] for item in second)
    return [item for item in first if item.attrib[comparator] not in second]


def generate_error(error_text):
    return {
        "response_type": "in_channel",
        "attachments": [
            {
                "fallback": "Error\n" + error_text,
                "title": "Error",
                "text": "```" + error_text + "```",
                "mrkdwn_in": [
                    "text"
                ],
                "color": "#CCCCCC"
            }
        ]
    }
