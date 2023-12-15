import re


class WebhookParser:
    edit_pattern = re.compile(r"\) edited \[.*?\]\(<(.*?)>\)")
    create_pattern = re.compile(r"\) created \[.*?\]\(<(.*?)>\)")
    delete_pattern = re.compile(r"\) deleted \[.*?\]\(<(.*?)>\)")

    def parse(content: str):
        if re.search(WebhookParser.edit_pattern, content):
            page_url = re.search(WebhookParser.edit_pattern, content).group(1)
            return "edit", page_url
        elif re.search(WebhookParser.create_pattern, content):
            page_url = re.search(
                WebhookParser.create_pattern, content).group(1)
            return "create", page_url
        elif re.search(WebhookParser.delete_pattern, content):
            page_url = re.search(
                WebhookParser.delete_pattern, content).group(1)
            return "delete", page_url
        else:
            return "", ""
