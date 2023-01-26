from datetime import datetime

import pandas as pd

from budget.models import Expense, Category
from excel.core.sheet_manager import SheetManager
from users.models import User

import socket

socket.setdefaulttimeout(150)


def populate_google_sheet_with_expenses_data(user):
    # Get user's expenses queryset
    expenses_queryset = Expense.objects.filter(users=user)

    # Create a dataframe from the queryset
    df = pd.DataFrame.from_records(expenses_queryset.values())

    # Rename columns to match Google Sheets column names
    df = df.rename(columns={'id': 'ID', 'created_at': 'Date', 'amount': 'Amount', 'category_id': 'Category ID'})

    # Add a new column for category name
    df['Category Name'] = df['Category ID'].apply(lambda x: Category.objects.get(pk=x).name)

    # Select only necessary columns
    df = df[['ID', 'Date', 'Category Name', 'Amount']]
    df['Date'] = df['Date'].apply(lambda x: datetime.strftime(x, '%Y-%m-%d'))
    df['Amount'] = df['Amount'].apply(lambda x: float(x))

    # Pivot the dataframe to have categories as columns
    df_pivot = df.pivot_table(index='Date', columns='Category Name', values='Amount', aggfunc='sum', fill_value=0,
                              margins=True, margins_name='All', dropna=True, sort=False).reset_index('Date')

    # Get the worksheet
    sheet_manager = SheetManager(user)
    worksheet = sheet_manager.create_or_get_sheet_by_month(clean=True)

    # Convert dataframe to a list of lists
    data = df_pivot.values.tolist()
    header = df_pivot.columns.tolist()

    data.insert(0, header)

    for i, row in enumerate(data):
        if i == 0:
            row[0] = f'{str(row[0])} (number of expenses)'
        elif i == len(data) - 1:
            pass
        else:
            expenses_for_date = expenses_queryset.filter(created_at__date=row[0])
            row[0] = f'{str(row[0])} ({len(expenses_for_date)})'

    worksheet.update('H1', 'Summary for all the expenses')
    worksheet.update('H3', [data[0]] + data[1:])

    df2 = df[['Date', 'Category Name', 'Amount']]
    worksheet.update('A1', 'Detailed expenses sorted by date')
    worksheet.update('A3', [df2.columns.values.tolist()] + df2.values.tolist())






def update_all_users_expenses_data():
    users_queryset = User.objects.all()

    for user in users_queryset:
        try:
            populate_google_sheet_with_expenses_data(user)
            print('Processed user: ', user.user_id)
        except Exception as ex:
            print(ex)