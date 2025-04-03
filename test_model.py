import os
from openai import OpenAI

client = OpenAI(base_url="http://127.0.0.1:1234", api_key="lm-studio")

prompt = """### Task
Generate a SQL query that answers the following question based on the database schema provided.

### Database Schema
Table: students
Columns:
- student_id (integer, primary key)
- name (varchar)
- age (integer)
- marks (decimal)
- grade (varchar)

### Question
Find all students who have more than 80% marks.

### SQL Query
"""

chat_completion = client.chat.completions.create(
    messages=[{"role": "user", "content": prompt}],
    model="sqlcoder-7b-2",
)

print(chat_completion.choices[0].message.content)
