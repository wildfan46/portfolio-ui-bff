import os
import boto3


ssm = boto3.client("ssm")


def get_param(name, decrypt=True):
    return ssm.get_parameter(
        Name=name, WithDecryption=decrypt
    )["Parameter"]["Value"]


def get_config():
    TODOIST_API_TOKEN = get_param(os.environ["TODOIST_PARAM"])
    PROFESSIONAL_PROJECT_ID = os.environ["PROFESSIONAL_PROJECT_ID"]
    GROWTH_SECTION_ID = os.environ["GROWTH_SECTION_ID"]
    return {
        "TODOIST_API_TOKEN": TODOIST_API_TOKEN,
        "PROFESSIONAL_PROJECT_ID": PROFESSIONAL_PROJECT_ID,
        "GROWTH_SECTION_ID": GROWTH_SECTION_ID,
    }
