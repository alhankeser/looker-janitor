import subprocess

TEST_FILE_DIR = "tests/test_files/"
DEFAULT_TYPE_ORDER = [
    "filter",
    "parameter",
    "dimension",
    "dimension_group",
    "measure",
    "set",
]


def files_match(a, b):
    with open(a) as file_a:
        with open(b) as file_b:
            return file_a.read() == file_b.read()


def setup_file_comparison_test(test_name):
    dir = TEST_FILE_DIR + test_name
    input_file_path = f"{dir}/input.view.lkml"
    output_file_path = f"{dir}/output.view.lkml"
    expected_file_path = f"{dir}/expected.view.lkml"
    subprocess.run(["cp", input_file_path, output_file_path])
    return output_file_path, expected_file_path


def test_order_field_types():
    output, expected = setup_file_comparison_test("test_order_field_types")
    subprocess.run(["python", "main.py", "--files", output])
    assert files_match(output, expected)


def test_multiple_files():
    output_a, expected_a = setup_file_comparison_test("test_multiple_files_a")
    output_b, expected_b = setup_file_comparison_test("test_multiple_files_b")
    subprocess.run(["python", "main.py", "--files", output_a, output_b])
    assert files_match(output_a, expected_a) and files_match(output_b, expected_b)


def test_type_order_param():
    output, expected = setup_file_comparison_test("test_type_order_param")
    subprocess.run(
        ["python", "main.py", "--files", output, "--type_order", "measure", "dimension"]
    )
    assert files_match(output, expected)


def test_param_order():
    output, expected = setup_file_comparison_test("test_param_order")
    subprocess.run(["python", "main.py", "--files", output])
    assert files_match(output, expected)


def test_param_order_param():
    output, expected = setup_file_comparison_test("test_param_order_param")
    subprocess.run(
        [
            "python",
            "main.py",
            "--files",
            output,
            "--param_order",
            "sql",
            "type",
        ]
    )
    assert files_match(output, expected)


def test_primary_key_first():
    output, expected = setup_file_comparison_test("test_primary_key_first")
    subprocess.run(["python", "main.py", "--files", output])
    assert files_match(output, expected)


def test_primary_key_first_param():
    output, expected = setup_file_comparison_test("test_primary_key_first_param")
    subprocess.run(
        ["python", "main.py", "--files", output, "--primary_key_first", "false"]
    )
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
    subprocess.run(
        ["python", "main.py", "--files", output, "--order_by_label", "false"]
    )
    assert files_match(output, expected)


def test_localization_file_path_param():
    output, expected = setup_file_comparison_test("test_localization_file_path_param")
    subprocess.run(
        [
            "python",
            "main.py",
            "--files",
            output,
            "--localization_file_path",
            "tests/test_files/test_localization_file_path_param/en.strings.json",
        ]
    )
    assert files_match(output, expected)


def test_order_field_parameters_param():
    output, expected = setup_file_comparison_test("test_order_field_parameters_param")
    subprocess.run(
        [
            "python",
            "main.py",
            "--files",
            output,
            "--order_field_parameters",
            "false",
        ]
    )
    assert files_match(output, expected)


def test_check_required_params_param():
    output, _ = setup_file_comparison_test("test_check_required_params_param")
    warnings = subprocess.check_output(["python", "main.py", "--files", output])
    assert len(warnings) == 0
    warnings = subprocess.check_output(
        ["python", "main.py", "--files", output, "--check_required_params", "true"]
    ).decode("utf-8")
    assert warnings == "\n"
    warnings = subprocess.check_output(
        [
            "python",
            "main.py",
            "--files",
            output,
            "--check_required_params",
            "true",
            "--required_dimension",
            "label",
        ]
    ).decode("utf-8")
    assert "output.view.lkml:14: dimension 'b_dimension_name' missing label" in warnings
    warnings = subprocess.check_output(
        [
            "python",
            "main.py",
            "--files",
            output,
            "--check_required_params",
            "true",
            "--required_dimension",
            "label sql hidden",
        ]
    ).decode("utf-8")
    assert "tests/test_files/test_check_required_params_param/output.view.lkml:10: dimension 'a_dimension_name' missing label sql hidden" in warnings
