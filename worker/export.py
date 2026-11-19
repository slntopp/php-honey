"""Nightly stock export: sends each retail outlet its batches as a CSV."""

import argparse

import requests
import yaml
from jinja2 import Environment, FileSystemLoader

HONEYFLOW = "http://web/index.php"


def load_outlets(path):
    with open(path) as f:
        return yaml.load(f)


def batches_for(outlet):
    resp = requests.get(HONEYFLOW, params={"action": "batches", "varietal": outlet["varietal"]})
    resp.raise_for_status()
    return resp.json()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--outlets", required=True)
    args = parser.parse_args()

    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("stock.csv.j2")
    for outlet in load_outlets(args.outlets)["outlets"]:
        body = template.render(outlet=outlet, batches=batches_for(outlet))
        requests.post(outlet["inbox"], data=body.encode(), verify=False)


if __name__ == "__main__":
    main()
