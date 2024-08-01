[![Action Tests](https://github.com/alhankeser/looker-janitor/actions/workflows/action_tests.yml/badge.svg)](https://github.com/alhankeser/looker-janitor/actions/workflows/action_tests.yml)[![Python Tests](https://github.com/alhankeser/looker-janitor/actions/workflows/tests.yml/badge.svg)](https://github.com/alhankeser/looker-janitor/actions/workflows/tests.yml)

## Looker Janitor
Clean your Looker LookML view files:
- Order field types (e.g. filters, dimensions, measures)
- Order fields (including by label and localized labels if need be)
- Order field parameters (e.g. type, label, description, sql...)
- Move primary key to top of dimensions list
- Check for missing field parameters and report in `%f:%l: %m` format

## Getting Started

As a local script:
```shell
python main.py example.view.lkml
```

As a GitHub action:
```shell
- name: Run Looker Janitor
  uses: alhankeser/looker-janitor-action@v0
```

## Testing

Run the following command:
```
pytest
```

## Read More about how to use Looker Janitor here:
[Looker Janitor: LookML View Cleaner](https://github.com/marketplace/actions/looker-janitor-lookml-view-cleaner)

## More examples

Override the default field type ordering and put dimensions above filters:
```shell
python main.py --files samples/example_input.view.lkml --type_order dimension filter measure 
```

Turn off type ordering entirely:
```shell
python main.py --files samples/example_input.view.lkml --order_types false
```

Provide a localization filepath to order labels by localized label value:
```shell
python main.py --files samples/example_input.view.lkml --localization_file_path samples/en.strings.json
```

Don't order fields by their labels and instead use field names:
```shell
python main.py --files samples/example_input.view.lkml --order_fields_by_label false
```

Turn off field ordering entirely:
```shell
python main.py --files samples/example_input.view.lkml --order_fields false
```

Set an order in which field parameters should be sorted:
If only a subset of paraters are provided, all remaining parameters will remain in their current order.
```shell
python main.py --files samples/example_input.view.lkml --param_order type label description sql
```

Override the default and don't put primary key first in list of dimensions:
```shell
python main.py --files samples/example_input.view.lkml --primary_key_first false  
```

Check for required parameters and specify what parameters are required for measures:
```shell
python main.py --files samples/example_input.view.lkml \
--check_required_params true \
--required_dimension type label \
--required_measure value_format_name
```
The following will get printed out:
```
samples/example_input.view.lkml:29: dimension 'customer_id' missing label
samples/example_input.view.lkml:34: dimension 'order_date' missing label
samples/example_input.view.lkml:39: dimension 'order_status' missing label
samples/example_input.view.lkml:52: measure 'average_order_value' missing value_format_name
samples/example_input.view.lkml:59: measure 'count' missing value_format_name
samples/example_input.view.lkml:65: measure 'total_sales' missing value_format_name
```

## Default settings

Below are the default settings for each parameter:

**type_order**:
- filter
- parameter
- dimension
- dimension_group
- measure
- set

**param_order**:
- hidden
- type
- view_label
- group_label
- group_item_label
- label
- description
- sql
- sql_start
- sql_end
- value_format_name
- value_format
- filters
- drill_fields

**primary_key_first**:
- true

**order_fields_by_label**:
- true

**order_types**:
- true

**order_fields**:
- true

**order_field_parameters**:
- true

**check_required_params**:
- false
