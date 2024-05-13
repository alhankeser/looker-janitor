import sys
import re

TYPE_ORDER = [
    'filter',
    'parameter',
    'dimension',
    'measure',
    'set'
]

def filter_fields_dict_by_type(field_type, fields_dict):
    return sorted([key for key, val in fields_dict.items() if val['field_type'] == field_type])

def get_distinct_field_types(fields_dict):
    distinct_types = set(val['field_type'] for val in fields_dict.values())
    sorted_types = sorted(distinct_types, key=lambda x: TYPE_ORDER.index(x) if x in TYPE_ORDER else -1)
    return sorted_types

def get_fields_dict(file_content):
    field_regex = r"(\w+):\s*(\w+)\s*{((?:[^{}]|(?:\${[^{}]*?}))*?)}"
    matching_fields = re.findall(field_regex, file_content, re.DOTALL)
    remaining_content = re.sub(field_regex, "", file_content)
    fields_dict = {}
    for field_type, field_name, field_content in matching_fields:
        fields_dict[field_name] = {
            'field_type': field_type,
            'field_content': field_content,
        }
    return fields_dict, re.sub(r'\n\s*\n', '\n', remaining_content)

def sort_fields(file_path):
    with open(file_path, 'r') as file:
        file_content = file.read()
        fields_dict, remaining_content = get_fields_dict(file_content)
        closing_tag_index = remaining_content.rfind('}')
        file.close()
    
    fields_content = ""
    for field_type in get_distinct_field_types(fields_dict):
        for field_name in filter_fields_dict_by_type(field_type, fields_dict):
            field = fields_dict[field_name]
            fields_content += f"  {field_type}: {field_name} {{ {field['field_content']}}}\n\n"
    with open("output.view.lkml", "w") as file:
        file.write(remaining_content[:closing_tag_index] + fields_content + remaining_content[closing_tag_index:])

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