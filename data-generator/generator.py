"""
Copyright 2018 Dawid Bautsch
dawid@bautsch.pl

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions
of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""


import argparse
import numpy.random
import csv


def generate_expensive_rows(total_rows):
    return numpy.random.random_integers(1, (total_rows / 100.0) * 1)


def generate_expensive_mode():
    expensive_mode = numpy.random.uniform(0, 1.0)

    if expensive_mode >= 0.5:
        return False

    return True


def generate_spread():
    min_spread_percent = 1.0
    max_spread_percent = 3.0

    return numpy.random.uniform(min_spread_percent, max_spread_percent)


def generate_currency_value(expensive_mode,
                            currency,
                            previous):
    min_step_percent = 0.4
    max_step_percent = 0.7

    spread = generate_spread()
    step = numpy.random.uniform(min_step_percent, max_step_percent)
    step_value = (previous / 100.0) * step

    if expensive_mode:
        selling_value = previous + step_value
    else:
        selling_value = previous - step_value

    buying_value = selling_value - ((selling_value / 100.0) * spread)

    return {
        'currency': currency,
        'selling_value': selling_value,
        'buying_value': buying_value,
        'spread': spread,
        'step': step,
        'expensive_mode': expensive_mode
    }


def generate_rows(how_much, currency, initial_value):
    generated_rows = []
    expensive_mode = False
    expensive_rows_left = 0
    previous = initial_value

    for i in range(0, how_much):
        if expensive_rows_left == 0:
            expensive_rows_left = generate_expensive_rows(how_much)
            expensive_mode = generate_expensive_mode()

        row = generate_currency_value(expensive_mode, currency, previous)
        generated_rows.append(row)
        previous = row['selling_value']
        expensive_rows_left = expensive_rows_left - 1

    return generated_rows


def write_rows(generated_rows, filename):
    try:
        with open(filename, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=';')
            for row in generated_rows:
                writer.writerow([row['currency'],
                                row['selling_value'],
                                row['buying_value'],
                                row['spread'],
                                row['step'],
                                str(row['expensive_mode'])])
    except Exception as e:
        print(str(e))


parser = argparse.ArgumentParser(description="Fake data generator for CinkciarzML.")
parser.add_argument("rows", type=int, help="Number of data rows to generate.")
parser.add_argument("currency", type=str, help="Name of currency for generated rows.")
parser.add_argument("out_filename", type=str, help="Name of an output file.")
parser.add_argument("initial_value", type=float, help="Initial value of currency.")
parser.add_argument("--show_plot", type=bool, help="Show plot using matplotlib.")

args = parser.parse_args()

rows = generate_rows(args.rows, args.currency, args.initial_value)
write_rows(rows, args.out_filename)

