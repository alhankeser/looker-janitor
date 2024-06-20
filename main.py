import regex as re
import argparse
import json
import sys

DEFAULT_TYPE_ORDER = [
    "filter",
    "parameter",
    "dimension",
    "dimension_group",
    "measure",
    "set",
]
DEFAULT_PARAM_ORDER = [
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
PATTERNS = [
    {"name": "braces", "pattern": r"(\{(?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*\})"},
    {"name": "brackets", "pattern": r"(\[[^[\]]*\])"},
    {"name": "quotes", "pattern": r"(\"(?:\\.|[^\"])*\"|'(?:\\.|[^\'])*')"},
    {"name": "no_quotes", "pattern": r"(\w+)"},
    {"name": "double_semicolon", "pattern": r"([\W|\w]*?);;"},
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
    return filtered_list


def sort_fields(fields):
    sorted_list = sorted(fields, key=lambda x: x["sort_key"].lower())
    if ARGS.primary_key_first:
        sorted_list = sorted(
            sorted_list,
            key=lambda x: x["is_primary_key"],
            reverse=True,
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


def get_params(params):
    params_sorted_by_original_order = [
        x["param_type"]
        for x in sorted(params, key=lambda x: x["param_original_position"])
    ]
    if ARGS.order_field_parameters:
        remaining_params = [
            x for x in params_sorted_by_original_order if x not in ARGS.param_order
        ]
        return ARGS.param_order + remaining_params
    return [x for x in params_sorted_by_original_order]


def get_types():
    if ARGS.type_order:
        remaining_types = [k for k in DEFAULT_TYPE_ORDER if k not in ARGS.type_order]
        return ARGS.type_order + remaining_types
    return DEFAULT_TYPE_ORDER


def get_required_params():
    if ARGS.check_required_params:
        return {
            "filter": ARGS.required_filter,
            "parameter": ARGS.required_parameter,
            "dimension": ARGS.required_dimension,
            "dimension_group": ARGS.required_dimension_group,
            "measure": ARGS.required_measure,
            "set": ARGS.required_set,
        }
    return {
        "filter": [],
        "parameter": [],
        "dimension": [],
        "dimension_group": [],
        "measure": [],
        "set": [],
    }


def get_localization_data():
    localization_data = {}
    if not ARGS.localization_file_path == "None":
        with open(ARGS.localization_file_path) as file_text:
            localization_data = json.load(file_text)
    return localization_data


def get_field_sort_key(field, localization_data):
    sort_key = field["field_name"]
    if ARGS.order_by_label and not field["label"] == "":
        label = re.search(rf"[\"|\']([\w|\W]+)[\"|\']", field["label"]).group(1)
        if label in localization_data.keys():
            label = localization_data[label]
        sort_key = label
    return sort_key


def get_field_params(fields):
    pattern_field_lookup = get_pattern_field_lookup()
    localization_data = get_localization_data()
    for field in fields:
        field["params"] = []
        field["label"] = ""
        start_index = field["fields_content"].find("{")
        end_index = field["fields_content"].rfind("}")
        original_fields_content = field["fields_content"][
            start_index + 1 : end_index - 1
        ]
        fields_content = original_fields_content
        if len(fields_content) == 0:
            continue
        for pattern in PATTERNS:
            params = pattern_field_lookup[pattern["name"]]
            for param_type in sort_params_by_len(params):
                param_search_pattern = param_type + "\\s*:\\s*" + pattern["pattern"]
                match = re.search(rf"{param_search_pattern}", fields_content)
                while match:
                    original_position, _ = re.search(
                        rf"{param_search_pattern}", original_fields_content
                    ).span()
                    field["params"].append(
                        {
                            "param_type": param_type,
                            "param_content": match.group(),
                            "param_original_position": original_position,
                        }
                    )
                    if param_type == "label":
                        field["label"] = match.group().strip()
                    fields_content = fields_content.replace(match.group(), "")
                    match = re.search(rf"{param_search_pattern}", fields_content)
        field["field_remaining_content"] = fields_content.strip()
        field["sort_key"] = get_field_sort_key(field, localization_data)
    return fields


def get_fields_content(fields, line_number_offset=0, warnings=[]):
    fields_content = ""
    required_params = get_required_params()
    for field_type in get_types():
        for field in filter_fields_by_type(field_type, fields):
            required_params_for_type = required_params[field_type]
            field_name = field["field_name"]
            fields_content += "\n  " + field_type + ": " + field_name + " {"
            for param_type in get_params(field["params"]):
                for param_in_field in filter_params_by_type(
                    field["params"], param_type
                ):
                    fields_content += "\n    " + param_in_field["param_content"]
                    param_type = param_in_field["param_type"]
                    if param_type in required_params_for_type:
                        required_params_for_type.remove(param_type)
            if len(field["field_remaining_content"].strip()) > 0:
                fields_content += "\n    " + field["field_remaining_content"]
            fields_content += "\n  }\n"
            if len(required_params_for_type) > 0 and ARGS.check_required_params:
                line_number = fields_content.count("\n")
                warnings.append(
                    {
                        "line_number": line_number + line_number_offset,
                        "message": f"{field_type} '{field_name}' missing "
                        + ",".join(required_params_for_type),
                    }
                )
    return fields_content, warnings


def format_warnings(warnings, file_path):
    formatted = ""
    for warning in warnings:
        formatted += "{file_path}:{line_number}: {message}\n".format(
            file_path=file_path,
            line_number=warning["line_number"],
            message=warning["message"],
        )
    return formatted


def convert_str_to_bool(input_str):
    if isinstance(input_str, bool):
        return input_str
    if input_str.lower() in ("yes", "true", "t", "y", "1"):
        return True
    elif input_str.lower() in ("no", "false", "f", "n", "0"):
        return False
    return False


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--files",
        nargs="+",
        type=str,
        help="List of files to clean.",
        required=False,
        default=[],
    )

    parser.add_argument(
        "--type_order",
        nargs="+",
        type=str,
        help="Order of field types.",
        required=False,
        default=DEFAULT_TYPE_ORDER,
    )

    parser.add_argument(
        "--param_order",
        nargs="+",
        type=str,
        help="Order of field parameters.",
        required=False,
        default=DEFAULT_PARAM_ORDER,
    )

    parser.add_argument(
        "--primary_key_first",
        type=convert_str_to_bool,
        help="Should primary key be ordered first.",
        required=False,
        default=True,
    )

    parser.add_argument(
        "--order_by_label",
        type=convert_str_to_bool,
        help="Should fields be ordered by their labels.",
        required=False,
        default=True,
    )

    parser.add_argument(
        "--localization_file_path",
        type=str,
        help="Path to localization file, used for field sorting.",
        required=False,
        default="None",
    )

    parser.add_argument(
        "--order_fields",
        type=convert_str_to_bool,
        help="Should fields be ordered.",
        required=False,
        default=True,
    )

    parser.add_argument(
        "--order_field_parameters",
        type=convert_str_to_bool,
        help="Should field parameters be ordered.",
        required=False,
        default=True,
    )

    parser.add_argument(
        "--check_required_params",
        type=convert_str_to_bool,
        help="Should required parameters be checked.",
        required=False,
        default=False,
    )

    parser.add_argument(
        "--required_filter",
        nargs="+",
        type=str,
        help="List of required filter parameters.",
        required=False,
        default=[],
    )

    parser.add_argument(
        "--required_parameter",
        nargs="+",
        type=str,
        help="List of required parameter parameters.",
        required=False,
        default=[],
    )

    parser.add_argument(
        "--required_dimension",
        nargs="+",
        type=str,
        help="List of required dimension parameters.",
        required=False,
        default=[],
    )

    parser.add_argument(
        "--required_dimension_group",
        nargs="+",
        type=str,
        help="List of required dimension_group parameters.",
        required=False,
        default=[],
    )

    parser.add_argument(
        "--required_measure",
        nargs="+",
        type=str,
        help="List of required measure parameters.",
        required=False,
        default=[],
    )

    parser.add_argument(
        "--required_set",
        nargs="+",
        type=str,
        help="List of required set parameters.",
        required=False,
        default=[],
    )

    return parser.parse_args()


def main():

    warnings = []
    for file_path in ARGS.files:

        with open(file_path, "r") as file:
            file_content = file.read()
            fields, remaining_content = get_fields(file_content)
            fields = get_field_params(fields)
            if ARGS.order_fields:
                fields = sort_fields(fields)
            closing_tag_index = remaining_content.rfind("}")
            file.close()

        line_number_offset = remaining_content[:closing_tag_index].count("\n")
        fields_content, warnings = get_fields_content(
            fields, line_number_offset, warnings
        )

        with open(file_path, "w") as file:
            file.write(
                remaining_content[:closing_tag_index]
                + fields_content
                + remaining_content[closing_tag_index:]
            )
    if ARGS.check_required_params:
        print(format_warnings(warnings, file_path))

if __name__ == "__main__":
    ARGS = parse_args()
    main()
