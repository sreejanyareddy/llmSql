from django.shortcuts import render
from django.contrib import messages
from .forms import QueryForm
import requests

def generate_sql_query(input_text, temper, db_schema):
    prompt = f"""### Database Schema:
{db_schema}

### Question:
{input_text}

### SQL:
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


# system promt using v1/chat/completions 

# from django.shortcuts import render
# from django.contrib import messages
# from .forms import QueryForm
# import requests

# def generate_sql_query(input_text, temper, db_schema):
#     system_prompt = """
# You are a helpful AI assistant expert in querying SQL Databases to find answers to user's questions.
# 1. Create and return a syntactically correct SQL query.
# 2. Limit results to 10 rows unless asked otherwise.
# 3. Prefer specific columns and relevant ordering.
# 4. Do not use INSERT, UPDATE, DELETE, or DROP.
# 5. If the question is meaningless, respond with "Meaningless".
# 6. If the question is unanswerable with the schema, respond with "I don't know".
# """

#     user_prompt = f"""
# ### Task
# Generate a SQL query to answer [QUESTION]{input_text}[/QUESTION]

# ### Database Schema
# {db_schema}

# ### Answer
# Given the database schema, here is the SQL query that answers [QUESTION]{input_text}[/QUESTION]
# [SQL]
# """

#     payload = {
#         "model": "sqlcoder-7b-2",
#         "messages": [
#             {"role": "system", "content": system_prompt},
#             {"role": "user", "content": user_prompt}
#         ],
#         "temperature": float(temper)
#     }

#     try:
#         response = requests.post("http://localhost:1234/v1/chat/completions", json=payload) 
#         result = response.json()

#         if 'choices' in result and len(result['choices']) > 0:
#             return result['choices'][0]['message']['content'].strip()
#         else:
#             return "Error: No valid response from the model."

#     except Exception as e:
#         return f"Error: {str(e)}"

# def index(request):
#     if request.method == 'POST':
#         form = QueryForm(request.POST)
#         if form.is_valid():
#             user_text = form.cleaned_data['user_text']
#             temper = form.cleaned_data['temperature']
#             db_schema = form.cleaned_data['db_schema']
#             sql_query = generate_sql_query(user_text, temper, db_schema)
#             return render(request, 'index.html', {
#                 'form': form,
#                 'sql_query': sql_query,
#                 'user_text': user_text
#             })
#     else:
#         form = QueryForm()
#     return render(request, 'index.html', {'form': form})



# system promt using v1/completions 

# from django.shortcuts import render
# from django.contrib import messages
# from .forms import QueryForm
# import requests

# def generate_sql_query(input_text, temper, db_schema):
#     prompt = f"""
# You are a helpful AI assistant expert in querying SQL Databases to find answers to user's questions.
# 1. Create and return a syntactically correct SQL query.
# 2. Limit results to 10 rows unless asked otherwise.
# 3. Prefer specific columns and relevant ordering.
# 4. Do not use INSERT, UPDATE, DELETE, or DROP.
# 5. If the question is meaningless, respond with "Meaningless".
# 6. If the question is unanswerable with the schema, respond with "I don't know".

# ### Database Schema:
# {db_schema}

# ### Question:
# {input_text}

# ### SQL:
# """

#     payload = {
#         "model": "sqlcoder-7b-2",
#         "prompt": prompt,
#         "temperature": float(temper),
#         "max_tokens": 512,
#         "stop": ["###"]
#     }

#     try:
#         response = requests.post("http://localhost:1234/v1/completions", json=payload)
#         result = response.json()

#         if 'choices' in result and len(result['choices']) > 0:
#             return result['choices'][0]['text'].strip()
#         else:
#             return "Error: No valid response from the model."

#     except Exception as e:
#         return f"Error: {str(e)}"


# def index(request):
#     if request.method == 'POST':
#         form = QueryForm(request.POST)
#         if form.is_valid():
#             user_text = form.cleaned_data['user_text']
#             temper = form.cleaned_data['temperature']
#             db_schema = form.cleaned_data['db_schema']
#             sql_query = generate_sql_query(user_text, temper, db_schema)
#             return render(request, 'index.html', {
#                 'form': form,
#                 'sql_query': sql_query,
#                 'user_text': user_text
#             })
#     else:
#         form = QueryForm()
#     return render(request, 'index.html', {'form': form})
