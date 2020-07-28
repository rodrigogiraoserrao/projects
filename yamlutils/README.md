# YAMLUtils

A little tool to help me manage YAML headers on my blog's posts, you can read about it [here](https://mathspp.com/blog/yamlutils).

Run `python yamlutils.py -h` to get the help message.

This script attempts to merge YAML headers from `*.*.md` files in the path you specify (traversing the directory tree recursively if `-r` is set) and moves duplicated YAML headers to a `frontmatter.yaml` file.