from django.shortcuts import render
from openai import OpenAI
import psycopg2
from django.contrib import messages
from .forms import QueryForm

client = OpenAI(base_url="http://127.0.0.1:1234", api_key="lm-studio")

def generate_sql_query(input_text, temper, db_schema):
    prompt = f"""### Task
Generate a SQL query to answer [QUESTION]{input_text}[/QUESTION]

### Database Schema
The query will run on a database with the following schema:
{db_schema}

### Answer
Given the database schema, here is the SQL query that answers [QUESTION]{input_text}[/QUESTION]
[SQL]
"""

    try:
        completion = client.chat.completions.create(
            model="sqlcoder-7b-2",
            messages=[{"role": "user", "content": prompt}],
            temperature=temper,
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {str(e)}"

def index(request):
    if request.method == 'POST':
        form = QueryForm(request.POST)
        if form.is_valid():
            user_text = form.cleaned_data['user_text']
            temper = form.cleaned_data['temperature']
            db_schema = form.cleaned_data['db_schema']
            sql_query = generate_sql_query(user_text, temper, db_schema)
            return render(request, 'index.html', {'form': form, 'sql_query': sql_query})
    else:
        form = QueryForm()
    return render(request, 'index.html', {'form': form})
