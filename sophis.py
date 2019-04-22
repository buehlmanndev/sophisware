#!/usr/bin/python
import argparse
import csv
import datetime

__author__ = 'ChBuehlmann'


def parse_args():
    parser = argparse.ArgumentParser(description='This Script translates copy-paste CSV Files from Sophisweb to Banana CSV')
    parser.add_argument('-i', '--input', help='Input file name, file has to include the Headers', required=True)
    parser.add_argument('-o', '--output', help='Output file name', required=True)
    return parser.parse_args()


def transform(input_file, output_file):
    with open(input_file, encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter='\t')
        with open(output_file, 'w', encoding='utf-8', newline='') as outputFile:
            fieldnames = ['Date', 'Doc', 'Description', 'AccountDebit', 'AccountCredit', 'Amount']
            writer = csv.DictWriter(outputFile, fieldnames=fieldnames, delimiter='\t')
            writer.writeheader()

            for row in reader:
                writer.writerow({'Date': rewrite_date(row), 'Doc': row['Beleg Nr.'], 'Description': rewrite_header(row),
                                 'AccountDebit': '1020', 'AccountCredit': '3400', 'Amount': float(row['Rgn.-Betrag'].replace('\'',''))})


def rewrite_header(row):
    header_array = row['Betreff'].split('/ ')
    return header_array[1].strip() + ' (' + row['Rgn.Nr.'] + ') ' + header_array[0].strip()


def rewrite_date(row):
    return datetime.datetime.strptime(row['Valuta'], '%d.%m.%Y').strftime('%Y-%m-%d')


def main():
    args = parse_args()
    transform(args.input, args.output)
    print("Done.")


if __name__ == "__main__":
    main()
