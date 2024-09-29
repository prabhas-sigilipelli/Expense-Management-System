from backend import db_helper


def test_fetch_expenses_for_date():
    expenses = db_helper.fetch_expenses_for_date("2024-08-15")
    print(expenses)
    assert len(expenses) == 1
    assert expenses[0]['amount'] == 10.0







