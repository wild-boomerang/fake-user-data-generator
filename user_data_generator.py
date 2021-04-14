import sys
from faker import Faker
import argparse
import csv
import pandas
from collections import defaultdict


def positive_int(value):
    int_value = int(value)
    if int_value <= 0:
        raise argparse.ArgumentTypeError(f"invalid choice: {value} (choose positive integer (>0))")
    return int_value


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('records_num', type=positive_int)
    parser.add_argument('region', type=str, choices=['en_US', 'ru_RU', 'uk_UA'])
    return parser


def run_parser():
    parser = create_parser()
    namespace = parser.parse_args()
    return namespace


def generate_fake_data(records_num, region):
    fake_data = defaultdict(list)
    fake = Faker(locale=region, use_weighting=False)
    for _ in range(records_num):
        fake_data["name"].append(fake.name())
        fake_data["address"].append(fake.address().replace('\n', ', '))
        fake_data["phone_number"].append(fake.phone_number())
    return fake_data


def print_fake_data(fake_data):
    df_fake_data = pandas.DataFrame(fake_data)
    # Escape the delimiter characters in the data
    df_fake_data.to_csv(sys.stdout, sep=';', index=False, escapechar='\\', quoting=csv.QUOTE_NONE)
    # df_fake_data.to_csv(sys.stdout, sep=';', index=False)  # or wrap the data in quotes


def main():
    namespace = run_parser()
    fake_data = generate_fake_data(namespace.records_num, namespace.region)
    print_fake_data(fake_data)


if __name__ == '__main__':
    main()
