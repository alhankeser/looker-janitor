## Looker Janitor
Consistently clean-up your LookML.

![Screenshot 2024-05-27 at 22 37 38](https://github.com/alhankeser/looker-janitor/assets/15135669/370729c7-1777-4b18-9045-c7cfe2818975)

## Getting Started

```shell
python main.py example_input.view.lkml example_output.view.lkml
```

## Options

- `TYPE_ORDER`: list of field types, in the order that you would like them to appear in your lookml view file.
- `PARAM_ORDER`: list of parameters, in the other that you would like them to apear in each field. Any remaining parameters in a field will be appended, in alphabetical order.
- `REQUIRED_PARAMS`: parameters that are required for each field type. Warnings are returned as a dictionary, including line number for each number.
- `OPTIONS`:
  - `sort_fields`
  - `sort_field_parameters`
  - `check_required_params`
  - `primary_key_first`
