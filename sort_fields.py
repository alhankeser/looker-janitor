import sys
import re

TYPE_ORDER = ["filter", "parameter", "dimension", "dimension_group", "measure", "set"]
PARAM_ORDER = ["hidden", "type", "group_label", "group_item_label", "label", "description", "sql"]
OPTIONS = {
    "sort_fields": True,
    "sort_field_parameters": True,
}

PARAM_PATTERNS = {
    "no_quotes": r"(\w+)",
    "quotes": r"((?:'|\")(?:\w|\s)+(?:'|\"))",
    "brackets": r"(\[[^[\]]*\])",
    "braces": r"(\{(?:[^{}]|(?R))*\})",
    "double_semicolon": r"(.*?);;"
}

PARAM_PATTERN_LOOKUP = {
    "action": "braces",
    "alias": "brackets",
    "allow_approximate_optimization": "no_quotes",
    "allow_fill": "no_quotes",
    "allowed_value": "braces",
    "alpha_sort": "no_quotes",
    "approximate": "no_quotes",
    "approximate_threshold": "no_quotes",
    "bypass_suggest_restrictions": "no_quotes",
    "can_filter": "no_quotes",
    "case": "braces",
    "case_sensitive": "no_quotes",
    "convert_tz": "no_quotes",
    "datatype": "no_quotes",
    "default_value": "quotes",
    "description": "quotes",
    "direction": "quotes",
    "drill_fields": "brackets",
    "end_location_field": "no_quotes",
    "fanout_on": "no_quotes",
    "filters": "brackets",
    "full_suggestions": "no_quotes",
    "group_item_label": "quotes",
    "group_label": "quotes",
    "hidden": "no_quotes",
    "html": "double_semicolon",
    "intervals": "brackets",
    "label": "quotes",
    "label_from_parameter": "no_quotes",
    "link": "braces",
    "list_field": "no_quotes",
    "map_layer_name": "no_quotes",
    "order_by_field": "no_quotes",
    "percentile": "no_quotes",
    "precision": "no_quotes",
    "primary_key": "no_quotes",
    "required_access_grants": "brackets",
    "required_fields": "brackets",
    "skip_drill_filter": "no_quotes",
    "sql": "double_semicolon",
    "sql_distinct_key": "double_semicolon",
    "sql_end": "double_semicolon",
    "sql_latitude": "double_semicolon",
    "sql_longitude": "double_semicolon",
    "sql_start": "double_semicolon",
    "start_location_field": "no_quotes",
    "string_datatype": "no_quotes",
    "style": "no_quotes",
    "suggest_dimension": "no_quotes",
    "suggest_explore": "no_quotes",
    "suggest_persist_for": "quotes",
    "suggestable": "no_quotes",
    "suggestions": "brackets",
    "tags": "brackets",
    "tiers": "brackets",
    "timeframes": "brackets",
    "type": "no_quotes",
    "units": "no_quotes",
    "value_format": "quotes",
    "value_format_name": "no_quotes",
    "view_label": "quotes"
}

def filter_fields_by_type(field_type, fields):
    filtered_list = [item for item in fields if item["field_type"] == field_type]
    sorted_list = sorted(
        filtered_list,
        key=lambda x: (x["field_name"].lower()),
        reverse=(False),
    )
    sorted_list = sorted(
        sorted_list,
        key=lambda x: (x["is_primary_key"]),
        reverse=(True),
    )
    return sorted_list


def get_fields(file_content):
    field_regex = r"((filter|parameter|dimension|measure|set)\s*:\s*(\w+)\s*{)"
    matching_fields = re.findall(field_regex, file_content, re.DOTALL)
    fields = []
    remaining_content = file_content
    for field_first_line_complete, field_type, field_name in matching_fields:
        fields.append(
            {
                "field_name": field_name,
                "field_type": field_type,
                "start_index": file_content.find(field_first_line_complete),
            }
        )
    for i, field in enumerate(fields):
        if i < len(fields) - 1:
            fields[i]["end_index"] = (
                file_content[: fields[i + 1]["start_index"]].rfind("}") + 1
            )
        else:
            parent_end_index = get_parent_end_index(file_content)
            fields[i]["end_index"] = file_content[:parent_end_index].rfind("}") + 1
        fields[i]["field_content"] = file_content[
            fields[i]["start_index"] : fields[i]["end_index"]
        ]
        fields[i]["is_primary_key"] = (
            fields[i]["field_content"].find("primary_key: yes") > -1
        )
    for field in fields:
        remaining_content = remaining_content.replace(field["field_content"], "")
    return fields, re.sub(r"\n\s*\n", "\n", remaining_content)


def get_parent_end_index(file_content):
    return file_content.rfind("}")

def get_field_params(fields):
    print(fields[:3])
#     attr_pattern = r"(?:" + "|".join(PARAM_ORDER) + ")\s*:"
#     print(attr_pattern)
#     for field in fields:
#         print(re.findall(attr_pattern,field["field_content"]))
                

def main():
    if len(sys.argv) != 2:
        print(f"Usage: python sort_fields.py <file_path>")
        return

    file_path = sys.argv[1]
    with open(file_path, "r") as file:
        file_content = file.read()
        fields, remaining_content = get_fields(file_content)
        get_field_params(fields)
        closing_tag_index = remaining_content.rfind("}")
        file.close()

    fields_content = ""
    for field_type in TYPE_ORDER:
        for field in filter_fields_by_type(field_type, fields):
            fields_content += "\n  " + field["field_content"] + "\n"
    with open("output.view.lkml", "w") as file:
        file.write(
            remaining_content[:closing_tag_index]
            + fields_content
            + remaining_content[closing_tag_index:]
        )
    return True

    # try:
    #     #
    # except FileNotFoundError:
    #     print("File not found.")
    # except Exception as e:
    #     print(e)


if __name__ == "__main__":
    main()
