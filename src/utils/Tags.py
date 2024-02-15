import sys
from src.configs import GLOBAL_CONFIG
import argparse


def validate_tag(tag, disable_reserved_tags):
    
    if tag not in GLOBAL_CONFIG.defined_tags:
        raise ValueError(f"Invalid tag specified. {tag} is not one of {GLOBAL_CONFIG.defined_tags}")

    if (disable_reserved_tags) and (tag in GLOBAL_CONFIG.reserved_tags):
        raise ValueError(f"Invalid tag specified, {tag} is a reserved tag.")

    pass

#checks for existance, whether it is defined, and if applicable whether it is reserved.
def validate_tag_args(args, tag_name, disable_reserved_tags):
    tag = getattr(args, tag_name)

    if not tag:
        raise ValueError(f"The flag --{tag_name} has not been specified, and is required.")

    validate_tag(tag, disable_reserved_tags)
    return tag


def get_tag_from_args(**kwargs):
    disable_reserved_tags = kwargs.get("disable_reserved_tags", False)
    parser = argparse.ArgumentParser()
    parser.add_argument('--tag', type=str)
    args = parser.parse_args()

    tag = validate_tag_args(args, 'tag', disable_reserved_tags)
    return tag


def get_tags_from_args(**kwargs):
    disable_reserved_tags = kwargs.get("disable_reserved_tags", False)
    parser = argparse.ArgumentParser()

    # Dynamically add tag arguments if you plan to scale this approach
    parser.add_argument('--tag_1', type=str)
    parser.add_argument('--tag_2', type=str)

    args = parser.parse_args()

    # Using a loop or directly calling a modular function for each tag
    tag_1 = validate_tag_args(args, 'tag_1', disable_reserved_tags)
    tag_2 = validate_tag_args(args, 'tag_2', disable_reserved_tags)

    return tag_1, tag_2





