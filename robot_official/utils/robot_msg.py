import re


def is_subscribe_msg(msg):
    match = re.match(r'^(订阅)(.*)', msg)
    return match.groups() if match else (None, None)

def is_unsubscribe_msg(msg):
    match = re.match(r'^(取消(?:订阅)?)(.*)', msg)
    return match.groups() if match else (None, None)