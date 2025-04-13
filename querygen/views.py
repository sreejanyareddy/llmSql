from django.shortcuts import render
from django.contrib import messages
from .forms import QueryFormWithoutSchema,QueryFormWithSchema
import requests
import psycopg2
import os


def home(request):
    return render(request, 'home.html')

# def query_db(request):
#     pass


# Read schema from a file
def read_schema_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            schema = file.read()
        return schema
    except Exception as e:
        return f"Error reading schema file: {str(e)}"



# 2. Execute the SQL query against the database
def execute_sql(query):
    try:
        conn = psycopg2.connect(
            dbname="22CS10040",   # Replace with your DB name
            user="22CS10040",   # Replace with your DB username
            password="22CS10040",   # Replace with your DB password
            host="10.5.18.70",   # or use your database host
            port="5432"         # Default PostgreSQL port
        )
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        colnames = [desc[0] for desc in cursor.description]
        cursor.close()
        conn.close()
        return rows, colnames
    except Exception as e:
        return [], [f"Execution Error: {str(e)}"]

# 3. query_db function: Handle natural query input and database response
def query_db(request):
    if request.method == 'POST':
        form = QueryFormWithoutSchema(request.POST)
        if form.is_valid():
            user_text = form.cleaned_data['user_text']
            temper = form.cleaned_data['temperature']

            # Step 1: Read schema from the file
            db_schema = f"""
                                        -- Table: students
                    CREATE TABLE students (
                        student_id SERIAL PRIMARY KEY,
                        name TEXT NOT NULL,
                        branch TEXT NOT NULL,
                        cgpa NUMERIC(3, 2),
                        graduation_year INT,
                        dob DATE                  -- New: date of birth
                    );
                    
                    -- Table: companies
                    CREATE TABLE companies (
                        company_id SERIAL PRIMARY KEY,
                        company_name TEXT NOT NULL,
                        domain TEXT,              -- e.g., "ml", "software", "finance"
                        visit_month TEXT,         -- e.g., "march"
                        offer_range TEXT          -- e.g., "10-20lpa", "20+lpa"
                    );
                    
                    -- Table: offers
                    CREATE TABLE offers (
                        offer_id SERIAL PRIMARY KEY,
                        student_id INT REFERENCES students(student_id),
                        company_id INT REFERENCES companies(company_id),
                        ctc NUMERIC(6, 2),        -- in LPA
                        role TEXT,
                        offer_date DATE
                    );
"""
            # Step 2: Generate the SQL query using the input and schema
            sql_query = generate_sql_query(user_text, temper, db_schema)

            # Step 3: If it's a SELECT query, execute it
            # if sql_query.lower().startswith(" SELECT"):
            rows, colnames = execute_sql(sql_query)
            return render(request, 'query_db.html', {
                    'form': form,
                    'sql_query': sql_query,
                    'rows': rows,
                    'colnames': colnames
                })
            # else:
            # messages.error(request, "Generated query is not a valid SELECT query.")
    else:
        form = QueryFormWithoutSchema()

    return render(request, 'query_db.html', {'form': form})


def generate_sql_query(input_text, temper, db_schema):
    system_prompt = f"""
You are a helpful AI assistant expert in querying SQL Database to find answers to user's question.
1. Create and execute a syntactically correct SQL Server query.
2. Limit the results to 10 unless specified otherwise.
3. Order the results by a relevant column to ensure the most interesting examples are returned.
4. Only request specific columns relevant to the query.
5. Not perform any Data Manipulation Language (DML) operations such as INSERT, UPDATE, DELETE, or DROP.
6. Double-check my queries before execution and provide a response based on the query results.
7. If a question doesn't relate to the database, I'll respond with "I don't know".
8. If a question is meaningless or empty, I'll respond with "Meaningless".
9. If the question is a generic greeting or small talk (e.g., "hello", "hi", "what's up"), respond with "I don't know".
10. If a question is valid and makes sense in English, but relates to a different database or domain not represented in the given schema, respond with "I don't know".
11. If the question contains valid English words but none of them match any word in the database schema (ignoring case), respond with "I don't know".
12. If the question contains gibberish or random characters (e.g., "sdfsd sdSFD"), respond with "Meaningless".
13. First classify the question. If it's valid and related to the schema, generate the SQL query. Otherwise, reply as per the above rules.
"""

    prompt = f"""{system_prompt}

### Database Schema:
{db_schema}

### Question:
{input_text}

### Response:
"""

    payload = {
        "prompt": prompt,
        "temperature": float(temper),
        "max_tokens": 512,
        "stop": ["###"]
    }

    try:
        response = requests.post("http://localhost:1234/v1/completions", json=payload)
        result = response.json()

        if 'choices' in result and len(result['choices']) > 0:
            return result['choices'][0]['text'].strip()
        else:
            return "Error: No valid response from the model."

    except Exception as e:
        return f"Error: {str(e)}"


def generate_sql(request):
    if request.method == 'POST':
        form = QueryFormWithSchema(request.POST)
        if form.is_valid():
            user_text = form.cleaned_data['user_text']
            temper = form.cleaned_data['temperature']
            db_schema = form.cleaned_data['db_schema']
            sql_query = generate_sql_query(user_text, temper, db_schema)
            return render(request, 'index.html', {'form': form, 'sql_query': sql_query})
    else:
        form = QueryFormWithSchema()
    return render(request, 'index.html', {'form': form})