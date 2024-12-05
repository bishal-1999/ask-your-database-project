from langchain_helper import fetch_table_and_related_schemas
from langchain.prompts import PromptTemplate
from database import fetch_schema
import re

####################################################################################################################################

query_template = """
<s>[INST] You are an expert at converting natural language questions into SQL queries for a MySQL database.
Your job is to generate accurate SQL queries based on the following database schema:

{schema}


Question: {question}
Generate the SQL query in MySQL format.
[/INST]</s> """

query_prompt_template = PromptTemplate.from_template(query_template)


####################################################################################################################################

def format_schema(schema):
    schema_str = ""
    for table, columns in schema.items():
        schema_str += f"Table: {table}\nColumns: {', '.join(columns)}\n\n"
    return schema_str.strip()


####################################################################################################################################

'''
def parse_sql_from_response(response_text):
    sql_pattern = re.compile(r"(SELECT|INSERT|UPDATE|DELETE).*?(;)", re.IGNORECASE | re.DOTALL)
    match = sql_pattern.search(response_text)
    return match.group(0).strip() if match else "No valid SQL query found."

'''


def parse_sql_from_response(response_text):
    # Improved regular expression
    sql_pattern = re.compile(r"(?i)\b(SELECT|INSERT|UPDATE|DELETE)\b.*?;", re.DOTALL)
    
    match = sql_pattern.search(response_text)
    
    if match:
        # Clean up any leading or trailing unwanted text (if it exists)
        sql_query = match.group(0).strip()
        return sql_query
    else:
        return "No valid SQL query found."

####################################################################################################################################

'''
def generate_sql_query(question, connection, llm):
    schema = fetch_schema(connection)
    if not schema:
        return "Error fetching schema."

    formatted_schema = format_schema(schema)
    formatted_prompt = query_prompt_template.format(schema=formatted_schema, question=question)

    print('\n\n',formatted_prompt,'\n\n')

    response = llm.stream(formatted_prompt)
    final_response = ''.join([res for res in response])
    
    return parse_sql_from_response(final_response.strip().replace("</s>", "").replace("<s>", ""))
'''

# updatd in 15.11.2024
def generate_sql_query(question, connection, llm, tables_list):
    
    tables_details = []
    if connection:
        for table_name in tables_list:
            schema = fetch_table_and_related_schemas(connection, table_name)
            tables_details.append(schema)

        # Set to track already processed tables
        processed_tables = set()
        formatted_output = ""

        for schema in tables_details:
            for table_name, table_data in schema.items():
                if table_name not in processed_tables:
                    # Format and append only if the table is not already processed
                    formatted_output += f"Table: {table_name}\n"
                    formatted_output += f"Columns: {', '.join(table_data['columns'])}\n"
                    if table_data['relationships']:
                        for rel in table_data['relationships']:
                            formatted_output += f"  Relationship: Column '{rel['column']}' -> Referenced Table: {rel['referenced_table']} -> Referenced Column: {rel['referenced_column']}\n"
                    else:
                        formatted_output += "  Relationships: No relationships\n"
                    formatted_output += "\n"  # Add spacing between tables
                    processed_tables.add(table_name)  # Mark the table as processed



    formatted_prompt = query_prompt_template.format(schema=formatted_output.strip(), question=question)

    print('\n formatted_prompt : ',formatted_prompt,'\n') # Debugging Statements

    response = llm.stream(formatted_prompt)
    final_response = ''.join([res for res in response])

    print('\n sql before parse : ',final_response.strip().replace("</s>", "").replace("<s>", "")) # Debugging Statements

    return parse_sql_from_response(final_response.strip().replace("</s>", "").replace("<s>", ""))


####################################################################################################################################







