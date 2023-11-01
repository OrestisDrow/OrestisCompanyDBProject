"""
def sales_over_time(conn, timeframe='monthly', start_date=None, end_date=None):
    time_grouping = {
        'daily': 'DateInfo.date',
        'weekly': "strftime('%Y-%W', DateInfo.date)",
        'monthly': "strftime('%Y-%m', DateInfo.date)"
    }

    query = f"""
#    SELECT {time_grouping[timeframe]} as period, SUM(Sales.quantity * Sales.unit_price) as total_sales
#    FROM Sales
#    JOIN DateInfo ON Sales.date_id = DateInfo.date_id
#    """
#    if start_date and end_date:
#        query += f" WHERE DateInfo.date BETWEEN '{start_date}' AND '{end_date}'"
#   query += f" GROUP BY {time_grouping[timeframe]} ORDER BY period"
#    df = pd.read_sql_query(query, conn)
#    return df.to_dict(orient="records")
#"""