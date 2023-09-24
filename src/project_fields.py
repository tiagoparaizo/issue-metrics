import os
import requests
from datetime import datetime, timedelta
from typing import List

from classes import IssueWithMetrics


def build_project_query(user, repository, number, project_fields):

    query = f"repo:{user}/{repository} is:issue number:{number}"
    field_queries = []

    for field_definition in project_fields:
        field_name = field_definition.get('name')
        field_type = field_definition.get('type')
        field_query = f"{field_name.replace(' ','_')}: fieldValueByName(name:\"{field_name}\") {{"
        
        if field_type == "Text":
            field_query += "... on ProjectV2ItemFieldTextValue { value: text }"
        elif field_type == "SingleSelect":
            field_query += "... on ProjectV2ItemFieldSingleSelectValue { value: name }"
        elif field_type == "Date":
            field_query += "... on ProjectV2ItemFieldDateValue { value: date }"
        elif field_type == "Iteration":
            field_query += "... on ProjectV2ItemFieldIterationValue { value: title }"
        elif field_type == "Number":
            field_query += "... on ProjectV2ItemFieldNumberValue { value: number }"
        elif field_type == "Number":
            field_query += "... on ProjectV2ItemFieldNumberValue { value: number }"

        field_query += "}"

        field_queries.append(field_query)

    project_query = f"project_fields: projectItems(first: 20) {{nodes{{"
    project_query += "".join(field_queries)
    project_query += "}}"

    graphql_query = """
    query{
        repository(name:"%s", owner: "%s") {
            issue(number: %s) {
                %s  # Inclui as queries dos projetos aqui
            }
        }
    }
    """ % (repository, user, number, project_query)

    return graphql_query

def execute_query(query, token):
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    response = requests.post("https://api.github.com/graphql", headers=headers, json={"query": query})

    if response.status_code == 200:
        data = response.json()
        return data

def get_fields_values(owner, repository, number, project_fields):
    
    query = build_project_query(
        owner,
        repository,
        number,
        project_fields
    )

    project_fields = execute_query(query, os.getenv("GH_TOKEN"))
    project_fields_data = project_fields["data"]["repository"]["issue"]["project_fields"]["nodes"]
    if len(project_fields_data) > 0:
        project_fields_data = project_fields_data[0]
        for key, value in project_fields_data.items():
            if value is not None and "value" in value:
                project_fields_data[key] = value["value"]
            elif value is None:
                project_fields_data[key] = None
        return project_fields_data
    else:
        return {}

    
