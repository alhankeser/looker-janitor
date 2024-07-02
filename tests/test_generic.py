import subprocess
from test_utils import setup_file_comparison_test, files_match

# AUTO-GENERATED GENERIC TESTS START BELOW THIS LINE 

def test_order_field_types():
    output, expected = setup_file_comparison_test("test_order_field_types")
    subprocess.run(["python", "main.py", "--files", output])
    assert files_match(output, expected)

def test_type_order_param():
    output, expected = setup_file_comparison_test("test_type_order_param")
    subprocess.run(["python", "main.py", "--files", output, "--type_order", "measure", "dimension"])
    assert files_match(output, expected)


def test_param_order():
    output, expected = setup_file_comparison_test("test_param_order")
    subprocess.run(["python", "main.py", "--files", output])
    assert files_match(output, expected)


def test_param_order_param():
    output, expected = setup_file_comparison_test("test_param_order_param")
    subprocess.run(["python", "main.py","--files",output,"--param_order","sql","type",])
    assert files_match(output, expected)


def test_primary_key_first():
    output, expected = setup_file_comparison_test("test_primary_key_first")
    subprocess.run(["python", "main.py", "--files", output])
    assert files_match(output, expected)


def test_primary_key_first_param():
    output, expected = setup_file_comparison_test("test_primary_key_first_param")
    subprocess.run(["python", "main.py", "--files", output, "--primary_key_first", "false"])
    assert files_match(output, expected)


def test_order_fields():
    output, expected = setup_file_comparison_test("test_order_fields")
    subprocess.run(["python", "main.py", "--files", output])
    assert files_match(output, expected)


def test_order_fields_param():
    output, expected = setup_file_comparison_test("test_order_fields_param")
    subprocess.run(["python", "main.py", "--files", output, "--order_fields", "false"])
    assert files_match(output, expected)


def test_order_by_label():
    output, expected = setup_file_comparison_test("test_order_by_label")
    subprocess.run(["python", "main.py", "--files", output])
    assert files_match(output, expected)


def test_order_by_label_param():
    output, expected = setup_file_comparison_test("test_order_by_label_param")
    subprocess.run(["python", "main.py", "--files", output, "--order_fields_by_label", "false"])
    assert files_match(output, expected)


def test_localization_file_path_param():
    output, expected = setup_file_comparison_test("test_localization_file_path_param")
    subprocess.run(["python", "main.py","--files",output,"--localization_file_path","tests/test_files/test_localization_file_path_param/en.strings.json",])
    assert files_match(output, expected)


def test_order_field_parameters_param():
    output, expected = setup_file_comparison_test("test_order_field_parameters_param")
    subprocess.run(["python", "main.py","--files",output,"--order_field_parameters","false",])
    assert files_match(output, expected)