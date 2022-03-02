#!/usr/bin/python
import argparse
import csv
import datetime

__author__ = 'ChBuehlmann'


def parse_args():
    parser = argparse.ArgumentParser(
        description='This Script translates sage 50 beam NT CSV Files from Sophisweb to Banana CSV (to be imported as txt file)')
    parser.add_argument('-i', '--input', help='Input file name, file has to include the Headers', required=True)
    return parser.parse_args()


def transform(input_file, output_file):
    with open(input_file, encoding='cp1252') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        with open(output_file, 'w', encoding='utf-8', newline='') as outputFile:
            fieldnames = ['Date', 'Doc', 'Description', 'AccountDebit', 'AccountCredit', 'Amount']
            writer = csv.DictWriter(outputFile, fieldnames=fieldnames, delimiter='\t')
            writer.writeheader()

            for count, row in enumerate(reader, start=1):
                if count % 2 == 1:  # every second Line
                    writer.writerow({'Date': rewrite_date(row['Datum']), 'Doc': row['Blg'], 'Description': row['Tx1'],
                                     'AccountDebit': '1020', 'AccountCredit': '3400',
                                     'Amount': float(row['Netto'].replace('\'', ''))})


def rewrite_date(datum_):
    return datetime.datetime.strptime(datum_, '%d.%m.%Y').strftime('%Y-%m-%d')


def main():
    args = parse_args()
    transform(args.input, args.input.replace('.csv', '_BANANA.txt'))
    print("Done.")


if __name__ == "__main__":
    main()
