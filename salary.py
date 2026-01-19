#!/usr/bin/env python3
"""

Usage:
   salary.py [mon|year|hou] [cad|usd|eur|gbp] <amount>

"""

import sys
import re
import os

from rich.table import Table
from rich.console import Console

DEBUG = os.getenv('DEBUG', '0') == '1'

exchange_rate = {
    'CADCZK': 15.01,
    'USDCZK': 20.83,
    'EURCZK': 24.25,
    'GBPCZK': 27.98,
    'CZKCZK': 1.0
}

TYPE = 'yearly'
CURRENCY = 'EUR'
AMOUNT = 0
HOURLY_RATE = 0


def detect_type():
    prefixes = {
        'mon': 'monthly',
        'year': 'yearly',
        'hou': 'hourly',
        'yr': 'yearly',
        'hr': 'hourly',
        'md': 'daily',
        'day': 'daily'
    }

    for arg in sys.argv:
        for p in prefixes:
            if arg.startswith(p):
                sys.argv.remove(arg)
                return prefixes[p]

    return None


def detect_currency():
    for i in sys.argv:
        if i.startswith('cad'):
            CURRENCY = 'CAD'
            break
        elif i.startswith('usd'):
            CURRENCY = 'USD'
            break
        elif i.startswith('eur'):
            CURRENCY = 'EUR'
            break
        elif i.startswith('gbp'):
            CURRENCY = 'GBP'
            break
        elif i.startswith('czk'):
            CURRENCY = 'CZK'
            break

    sys.argv.remove(i)
    return CURRENCY


def currency_to_czk(amount, currency):
    key = currency + 'CZK'
    if key in exchange_rate:
        return amount * exchange_rate[key]
    else:
        print(f'Unknown currency {currency}, exiting...', file=sys.stderr)
        sys.exit(1)


def detect_amount():
    for arg in sys.argv:
        match = re.match(r'([0-9]+)', arg)
        if match:
            AMOUNT = int(match.group(1))
            sys.argv.remove(arg)
            return AMOUNT

    print('Amount not specified, exiting...', file=sys.stderr)
    sys.exit(1)


def calculate_hourly_czk(salary_czk):
    if TYPE == 'yearly':
        return salary_czk / 12 / (8 * 5 * 4)
    elif TYPE == 'monthly':
        return salary_czk / (8 * 5 * 4)
    elif TYPE == 'daily':
        return salary_czk / 8
    elif TYPE == 'hourly':
        return salary_czk


def calculate(label, formula):
    print(f"{label}:")
    for currency, rate in exchange_rate.items():
        curr = currency.replace("CZK", "", 1)
        value = formula(rate)
        print(f"  {curr}: {value:.2f}")

########
# Main #
########


sys.argv.pop(0)  # remove script name
# Convert all sys.arv to lower case
sys.argv = [arg.lower() for arg in sys.argv]

if '-h' in sys.argv or '--help' in sys.argv:
    print(__doc__)
    sys.exit(0)

TYPE = detect_type()
CURRENCY = detect_currency()
AMOUNT = detect_amount()
if len(sys.argv) > 0:
    print(f'Invalid  arguments {sys.argv}, exiting...', file=sys.stderr)
    sys.exit(1)

HOURLY_RATE = calculate_hourly_czk(currency_to_czk(AMOUNT, CURRENCY))

if DEBUG:
    print(f'Detected type: {TYPE}')
    print(f'Detected currency: {CURRENCY}')
    print(f'Currency in CZK: ', currency_to_czk(AMOUNT, CURRENCY))
    print(f'Hourly rate in CZK: ', HOURLY_RATE)

    calculate("Yearly salary", lambda rate: HOURLY_RATE * 8 * 5 * 4 * 12 / rate)
    calculate("Monthly salary", lambda rate: HOURLY_RATE * 8 * 5 * 4 / rate)
    calculate("Man day", lambda rate: HOURLY_RATE * 8 / rate)
    calculate("Hourly rate", lambda rate: HOURLY_RATE / rate)


################
# Table Output #
################

table = Table(title="Salary Table")

table.add_column("Currency")
table.add_column("Hourly", justify="right")
table.add_column("Man Day", justify="right")
table.add_column("Monthly", justify="right")
table.add_column("Yearly", justify="right")

for currency in ["CZK", "CAD", "USD", "EUR", "GBP"]:
    table.add_row(
        currency,
        f"{HOURLY_RATE / exchange_rate[currency + 'CZK']:.2f}",
        f"{(HOURLY_RATE * 8) / exchange_rate[currency + 'CZK']:.2f}",
        f"{(HOURLY_RATE * 8 * 5 * 4) / exchange_rate[currency + 'CZK']:.2f}",
        f"{(HOURLY_RATE * 8 * 5 * 4 * 12) /
            exchange_rate[currency + 'CZK']:.2f}"
    )

Console().print(table)
