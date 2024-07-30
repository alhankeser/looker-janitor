import regex as re
import argparse
import json
import lkml
import subprocess

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


def get_fields(fields):
    if ARGS.order_fields:
        localization_data = get_localization_data()
        for i, field in enumerate(fields):
            fields[i] = get_params(field)
            has_label = "label" in fields[i]
            if (
                ARGS.primary_key_first
                and "primary_key" in field
                and field["primary_key"].lower() == "yes"
            ):
                fields[i]["sort_key"] = "-1"
            else:
                fields[i]["sort_key"] = (
                    fields[i]["label"]
                    if ARGS.order_fields_by_label and has_label
                    else fields[i]["name"]
                )
            if fields[i]["sort_key"] in localization_data:
                fields[i]["sort_key"] = localization_data[fields[i]["sort_key"]]
        fields = [
            {k: v for k, v in field.items() if k != "sort_key"}
            for field in sorted(fields, key=lambda x: x["sort_key"].lower())
        ]
    return fields


def get_params(field):
    if ARGS.order_field_parameters:
        sort_keys = {}
        original_params = list(field)
        custom_order_count = len(ARGS.param_order)
        for param_name in original_params:
            sort_keys[param_name] = (
                ARGS.param_order.index(param_name)
                if param_name in ARGS.param_order
                else (original_params.index(param_name) + custom_order_count)
            )
        sorted_params = [
            item for item in sorted(field.items(), key=lambda x: sort_keys[x[0]])
        ]
        field = dict(sorted_params)
    return field


def get_required_params():
    return {
        "filters": ARGS.required_filter,
        "parameters": ARGS.required_parameter,
        "dimensions": ARGS.required_dimension,
        "dimension_groups": ARGS.required_dimension_group,
        "measures": ARGS.required_measure,
        "sets": ARGS.required_set,
    }


def get_localization_data():
    localization_data = {}
    if not ARGS.localization_file_path == "None":
        with open(ARGS.localization_file_path) as file_text:
            localization_data = json.load(file_text)
    return localization_data


def get_field_sort_key(field, localization_data):
    sort_key = field["field_name"]
    if ARGS.order_fields_by_label and not field["label"] == "":
        label = re.search(rf"[\"|\']([\w|\W]+)[\"|\']", field["label"]).group(1)
        if label in localization_data:
            label = localization_data[label]
        sort_key = label
    return sort_key


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
        "--order_fields_by_label",
        type=convert_str_to_bool,
        help="Should fields be ordered by their labels.",
        required=False,
        default=True,
    )

    parser.add_argument(
        "--order_types",
        type=convert_str_to_bool,
        help="Should fields be ordered by their types.",
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


def get_field_types(view):
    if ARGS.order_types:
        ordered_types = [x + "s" for x in ARGS.type_order if x + "s" in view]
        remaining_types = [
            x for x in view if x[:-1] in DEFAULT_TYPE_ORDER and x not in ordered_types
        ]
        return ordered_types + remaining_types
    return [x for x in view if x[:-1] in DEFAULT_TYPE_ORDER]


def get_non_field_types(view):
    return [x for x in view if x[:-1] not in DEFAULT_TYPE_ORDER]


def check_required_params(required, view, warnings):
    for field_type, required_params in required.items():
        if field_type in view:
            for field in view[field_type]:
                if len(field) < len(set(list(field) + required_params)):
                    missing_params = [x for x in required_params if x not in field]
                    warnings.append(
                        {
                            "view_name": view["name"],
                            "field_type": field_type[:-1],
                            "field_name": field["name"],
                            "parameters": missing_params,
                        }
                    )
    return warnings


def get_field_regex(warning):
    view_name = warning["view_name"]
    field_type = warning["field_type"]
    field_name = warning["field_name"]
    return rf"view:\s{view_name}\s\{{[\s\S]*?({field_type}:\s{field_name}\s\{{[\s\S]*?\}}[\s\S]*?\}})"


def get_warning_line_numbers(warnings, lookml_out):
    for i, warning in enumerate(warnings):
        field_regex = get_field_regex(warning)
        match = re.search(field_regex, lookml_out)
        warnings[i]["line_number"] = lookml_out[: match.start(1)].count("\n")
    return warnings


def format_warnings(warnings, file_path):
    formatted_warnings = ""
    for warning in warnings:
        formatted_warnings += "{file_path}:{line_number}: [looker-janitor] {field_type} '{field_name}' missing {missing}\n".format(
            file_path=file_path,
            line_number=warning["line_number"],
            missing="".join(warning["parameters"]),
            field_name=warning["field_name"],
            field_type=warning["field_type"],
        )
    return formatted_warnings


def main():

    all_warnings = ""
    required_params = get_required_params()
    for file_path in ARGS.files:
        warnings = []
        with open(file_path, "r") as file:
            lookml = file.read()
            parsed_lookml = lkml.load(lookml)

        for i, view_in in enumerate(parsed_lookml["views"]):
            view_out = {}
            for field_type in get_non_field_types(view_in):
                view_out[field_type] = view_in[field_type]
            for field_type in get_field_types(view_in):
                view_out[field_type] = get_fields(view_in[field_type])

            parsed_lookml["views"][i] = view_out

            lookml_out = lkml.dump(parsed_lookml)

            if ARGS.check_required_params:
                warnings = check_required_params(required_params, view_out, warnings)
                warnings = get_warning_line_numbers(warnings, lookml_out)
                all_warnings += format_warnings(warnings, file_path)

        with open(file_path, "w") as file:
            file.write(lookml_out + "\n")

    if ARGS.check_required_params:
        print(all_warnings)


if __name__ == "__main__":
    ARGS = parse_args()
    main()
