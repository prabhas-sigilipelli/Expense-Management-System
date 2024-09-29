import mysql.connector
from contextlib import contextmanager
from logging_setup import setup_logger

logger = setup_logger('db_helper')

@contextmanager
def get_db_cursor(commit=False):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456",
        database="expense_manager"
    )

    cursor = connection.cursor(dictionary=True)
    yield cursor
    if commit:
        connection.commit()
    cursor.close()
    connection.close()


def fetch_all_records():
    query = "SELECT * from expenses"

    with get_db_cursor() as cursor:
        cursor.execute(query)
        expenses = cursor.fetchall()
        for expense in expenses:
            print(expense)


def fetch_expenses_for_date(expense_date):
    logger.info(f"fetch_expenses_for_date called with {expense_date}")
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM expenses WHERE expense_date = %s", (expense_date,))
        expenses = cursor.fetchall()

        if not expenses:  # Check if expenses is empty
            print(f"No expenses found for date: {expense_date}")
            return None

        for expense in expenses:
            print(expense)  # Print each expense for debugging

        return expenses  # Return the list of expenses if needed


def insert_expense(expense_date, amount, category, notes):
    logger.info(f"insert_expense called with date: {expense_date}, amount: {amount}, category: {category}, notes: {notes}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(
            "INSERT INTO expenses (expense_date, amount, category, notes) VALUES (%s, %s, %s, %s)",
            (expense_date, amount, category, notes)
        )


def delete_expenses_for_date(expense_date):
    logger.info(f"delete_expenses_for_date called with {expense_date}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute("DELETE FROM expenses WHERE expense_date = %s", (expense_date,))

def fetch_expense_summary(start_date,end_date):
    logger.info(f"fetch_expense_summary called with start: {start_date} end: {end_date}")
    with get_db_cursor() as cursor:
        cursor.execute(
            '''
                SELECT  SUM(amount) AS total, category
                FROM expense_manager.expenses
                WHERE expense_date BETWEEN  %s AND  %s
                GROUP BY  category;
                ''',
            (start_date,end_date)
        )
        data = cursor.fetchall()
        return data
def fetch_monthly_expenses():
    logger.info(f"fetch_expense_summary_by_months")
    with get_db_cursor() as cursor:
        cursor.execute(
            '''
                SELECT  MONTHNAME(expense_date) AS Month_Name ,SUM(amount) AS Total
                FROM expense_manager.expenses
                GROUP BY MONTHNAME(expense_date)
                ORDER BY MONTHNAME(expense_date) ;
                ''',

        )
        data = cursor.fetchall()
        return data


if __name__ == "__main__":
     # summary = fetch_expense_summary("2024-08-01","2024-08-05")
     # for record in summary:
     #     print(record)
     # expenses = fetch_expenses_for_date("2024-08-01")
     # print(expenses)

     total_amount = fetch_expense_months()
     print(total_amount)
