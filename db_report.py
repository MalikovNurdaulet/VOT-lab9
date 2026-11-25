import os
import pandas as pd
from sqlalchemy import create_engine

url = os.environ["DATABASE_URL"]
engine = create_engine(url)

group_by = os.getenv("GROUP_BY", "city")

if group_by not in ["city", "product"]:
    raise ValueError("GROUP_BY must be city or product")

query = f"""
SELECT
    {group_by},
    COUNT(*) AS sales,
    SUM(amount) AS revenue
FROM sales
GROUP BY {group_by}
ORDER BY revenue DESC
"""

print(pd.read_sql(query, engine).to_string(index=False))
