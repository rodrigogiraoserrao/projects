"""Utility script to manage YAML headers in my site (https://mathspp).
"""

import argparse
from pathlib import Path
import re
from ruamel import yaml

def recursively_trim_empty(d):
    """Recursively remove empty subdicts from a dictionary."""

    result = {}
    for key, value in d.items():
        if isinstance(value, dict) and value:
            subresult = recursively_trim_empty(value)
            if subresult:
                result[key] = subresult
        elif value != {}:
            result[key] = value
    return result

def recursive_dict_intersection(source, dest):
    """Intersect two dictionaries, going recursively into subdicts."""

    result = {}
    for key, value in source.items():
        if key in dest and not isinstance(value, dict) and value == dest[key]:
            result[key] = value
        elif isinstance(value, dict) and key in dest and isinstance(dest[key], dict):
            result[key] = recursive_dict_intersection(value, dest[key])
    return recursively_trim_empty(result)

def recursive_dict_union(base, extension):
    """Join two dictionaries, enter subdicts recursively."""

    result = {**base}
    for key, value in extension.items():
        if isinstance(value, dict) and key in result and isinstance(result[key], dict):
            result[key] = recursive_dict_union(result[key], value)
        else:
            result[key] = value
    return recursively_trim_empty(result)

def recursive_dict_difference(base, to_remove):
    """Find the difference of two dictionaries, enter subdicts recursively."""

    result = {}
    for key, value in base.items():
        if key not in to_remove:
            result[key] = value
        elif isinstance(value, dict) and isinstance(to_remove[key], dict):
            result[key] = recursive_dict_difference(value, to_remove[key])
        elif to_remove[key] != value:
            result[key] = value
    return recursively_trim_empty(result)

def extract_yaml_header(filepath):
    """Extract the yaml header from a .md file."""

    with open(filepath, "r", encoding="utf-8") as f:
        contents = f.read()
    match = re.match(r"^---\n((.|\n)*?\n)---", contents)
    return {} if not match else yaml.safe_load(match.group(1))

def replace_yaml_header(filepath, new_header):
    """Replace the yaml header of a file."""

    replace_with = (
        "---\n" +
        yaml.dump(
            new_header, indent=4, block_seq_indent=2,
            default_flow_style=False, allow_unicode=True
        ) +
        "---\n\n"
    ) if new_header else ""
    with open(filepath, "r+", encoding="utf-8") as f:
        contents = f.read()
        contents = re.sub(r"^---\n((.|\n)*?\n)---\n+", replace_with, contents)
        f.seek(0)
        f.truncate()
        f.write(contents)

def merge_yaml(folderpath, *, recursive):
    """Merge yaml header data from *.*.md files."""

    if recursive:
        hits = list({tuple(p.parent.glob("*.*.md")) for p in Path(folderpath).rglob("*.*.md")})
    else:
        hits = [tuple(Path(folderpath).glob("*.*.md"))]
    hits = filter(bool, hits)
    count = 0
    for hit in hits:
        # parse the YAML headers from all the files.
        collected = extract_yaml_header(hit[0])
        for h in hit[1:]:
            y = extract_yaml_header(h)
            collected = recursive_dict_intersection(collected, y)

        # check for a frontmatter.yaml file to dump the intersection.
        files = list(filter(
            lambda p: p.exists(),
            [hit[0].with_name("frontmatter.yaml"), hit[0].with_name("frontmatter.yml")]
        ))
        y = None
        if files:
            with open(files[0], "r", encoding="utf-8") as f:
                y = yaml.safe_load(f)
            dumpto = files[0]
        else:
            dumpto = hit[0].with_name("frontmatter.yaml")
        if y is None:
            y = {}

        print(y)
        dump = recursive_dict_union(y, collected)
        if not dump:
            continue

        with open(dumpto, "w", encoding="utf-8") as f:
            yaml.dump(
                dump, f, indent=4, block_seq_indent=2,
                default_flow_style=False, allow_unicode=True,
            )

        # go back and remove what was extracted.
        for h in hit:
            y = extract_yaml_header(h)
            new_y = recursive_dict_difference(y, dump)
            replace_yaml_header(h, new_y)

        print(".", end="")
        count += 1
    print(f" merged {count} locations.")

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("folder", help="Folder in which to process YAML merging")
    parser.add_argument("-r", action="store_true", help="Merge recursively in the folder.")

    args = parser.parse_args()
    merge_yaml(args.folder, recursive=args.r)
