from typing import Tuple, List, Optional
import datetime


class InvalidDateFormatError(Exception):
    pass


def process_payment(payment_string: str) -> Optional[Tuple[float, datetime.datetime, str]]:
    try:
        payment_parts = payment_string.split(',')
        amount = float(payment_parts[0].strip())
        date = datetime.date.today()
        category = None

        if len(payment_parts) > 1:
            category = payment_parts[1].strip().capitalize()

            if len(payment_parts) > 2:
                try:
                    date = datetime.datetime.strptime(payment_parts[2].strip(), '%Y-%m-%d')
                except ValueError:
                    return None

        return amount, date, category
    except Exception as ex:
        return None


def process_multiple_payments(payment_string: str):
    payments = []
    payment_strings = payment_string.split('\n')
    not_processed = []
    for s in payment_strings:
        processed = process_payment(s)
        if processed:
            payments.append(processed)
        else:
            not_processed.append(s)
    return payments, not_processed
