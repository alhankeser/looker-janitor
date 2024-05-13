import sys
import re

TYPE_ORDER = ["filter", "parameter", "dimension", "measure", "set"]


def filter_fields_by_type(field_type, fields):
    filtered_list = [item for item in fields if item["field_type"] == field_type]
    sorted_list = sorted(
        filtered_list,
        key=lambda x: (x["is_primary_key"], x["field_name"].lower()),
        reverse=(True, False),
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


def sort_fields(file_path):
    with open(file_path, "r") as file:
        file_content = file.read()
        fields, remaining_content = get_fields(file_content)
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


def main():
    if len(sys.argv) != 2:
        print(f"Usage: python sort_fields.py <file_path>")
        return

    file_path = sys.argv[1]
    sort_fields(file_path)

    # try:
    #     #
    # except FileNotFoundError:
    #     print("File not found.")
    # except Exception as e:
    #     print(e)


if __name__ == "__main__":
    main()
