import sys
import regex as re

TYPE_ORDER = ["filter", "parameter", "dimension", "dimension_group", "measure", "set"]
PARAM_ORDER = [
    "hidden",
    "type",
    "view_label",
    "group_label",
    "group_item_label",
    "label",
    "description",
    "sql",
    "sql_start",
    "sql_end",
    "value_format_name",
    "value_format",
    "filters",
    "drill_fields",
]
REQUIRED_PARAMS = {
    "filter": [],
    "parameter": [],
    "dimension": ["label"],
    "dimension_group": ["label"],
    "measure": ["label", "drill_fields"],
    "set": [],
}
OPTIONS = {
    "sort_fields": True,
    "sort_field_parameters": True,
    "check_required_params": True,
    "primary_key_first": True
}
PATTERNS = [
    {"name": "braces", "pattern": r"(\{(?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*\})"},
    {"name": "brackets", "pattern": r"(\[[^[\]]*\])"},
    {"name": "quotes", "pattern": r"((?:'|\")(?:\W|\w)[^\"]+(?:'|\"))"},
    {"name": "no_quotes", "pattern": r"(\w+)"},
    {"name": "double_semicolon", "pattern": r"(.*?);;"},
]
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
    "fields": "brackets",
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
    "view_label": "quotes",
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
    field_regex = (
        r"((filter|parameter|dimension|dimension_group|measure|set)\s*:\s*(\w+)\s*{)"
    )
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
        fields[i]["fields_content"] = file_content[
            fields[i]["start_index"] : fields[i]["end_index"]
        ]
        fields[i]["is_primary_key"] = (
            fields[i]["fields_content"].find("primary_key: yes") > -1
        )
    for field in fields:
        remaining_content = remaining_content.replace(field["fields_content"], "")
    return fields, re.sub(r"\n\s*\n", "\n", remaining_content)


def get_parent_end_index(file_content):
    return file_content.rfind("}")


def filter_patterns_by_name(pattern_name):
    return [x for x in PATTERNS if x["name"] == pattern_name][0]


def filter_fields_by_pattern(pattern_name):
    return [k for k, v in PARAM_PATTERN_LOOKUP.items() if v == pattern_name]


def filter_params_by_type(filter_params, param_type):
    return [x for x in filter_params if x["param_type"] == param_type]


def sort_params_by_len(params):
    return [x for x in sorted(params, key=len, reverse=True)]


def get_pattern_field_lookup():
    lookup = {}
    for pattern in PATTERNS:
        lookup[pattern["name"]] = filter_fields_by_pattern(pattern["name"])
    return lookup


def get_sorted_params():
    remaining_params = [k for k in PARAM_PATTERN_LOOKUP.keys() if k not in PARAM_ORDER]
    return PARAM_ORDER + remaining_params


def get_field_params(fields):
    pattern_field_lookup = get_pattern_field_lookup()
    for field in fields:
        field["params"] = []
        start_index = field["fields_content"].find("{")
        end_index = field["fields_content"].rfind("}")
        fields_content = field["fields_content"][start_index + 1 : end_index - 1]
        if len(fields_content) == 0:
            continue
        for pattern in PATTERNS:
            params = pattern_field_lookup[pattern["name"]]
            for param_type in sort_params_by_len(params):
                param_search_pattern = param_type + "\\s*:\\s*" + pattern["pattern"]
                match = re.search(rf"{param_search_pattern}", fields_content)
                while match:
                    field["params"].append(
                        {
                            "param_type": param_type,
                            "param_content": match.group(),
                        }
                    )
                    fields_content = fields_content.replace(match.group(), "")
                    match = re.search(rf"{param_search_pattern}", fields_content)
        field["field_remaining_content"] = fields_content.strip()
    return fields


def get_fields_content(fields, line_number_offset=0):
    fields_content = ""
    warnings = []
    for field_type in TYPE_ORDER:
        for field in filter_fields_by_type(field_type, fields):
            required_params = REQUIRED_PARAMS[field_type]
            field_name = field["field_name"]
            fields_content += "\n  " + field_type + ": " + field_name + " {"
            for param_type in get_sorted_params():
                for param_in_field in filter_params_by_type(
                    field["params"], param_type
                ):
                    fields_content += "\n    " + param_in_field["param_content"]
                    param_type = param_in_field["param_type"]
                    if param_type in required_params:
                        required_params.remove(param_type)
            if len(field["field_remaining_content"].strip()) > 0:
                fields_content += "\n    " + field["field_remaining_content"]
            fields_content += "\n  }\n"
            if len(required_params) > 0:
                line_number = fields_content.count("\n")
                warnings.append(
                    {
                        "line_number": line_number + line_number_offset,
                        "column_number": 0,
                        "message": f"{field_type} '{field_name}' missing " + ",".join(required_params)
                    }
                )
    return fields_content, warnings

def format_warnings(warnings, file_path):
    formatted = ""
    for warning in warnings:
        formatted += "{file_path}:{line_number}:{column_number}:{message}\n".format(
            file_path=file_path,
            line_number=warning["line_number"],
            column_number=warning["column_number"],
            message=warning["message"]
        )
    return formatted

def main():
    if len(sys.argv) < 2:
        print(f"Usage: python main.py <file_path>")
        return

    file_path = sys.argv[1]
    output_file_path = file_path

    if len(sys.argv) > 2:
        output_file_path = sys.argv[2]

    with open(file_path, "r") as file:
        file_content = file.read()
        fields, remaining_content = get_fields(file_content)
        fields = get_field_params(fields)
        closing_tag_index = remaining_content.rfind("}")
        file.close()

    line_number_offset = remaining_content[:closing_tag_index].count("\n")
    fields_content, warnings = get_fields_content(fields, line_number_offset)

    with open(output_file_path, "w") as file:
        file.write(
            remaining_content[:closing_tag_index]
            + fields_content
            + remaining_content[closing_tag_index:]
        )
    print(format_warnings(warnings, file_path))


if __name__ == "__main__":
    main()
