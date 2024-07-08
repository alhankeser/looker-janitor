import subprocess
from test_utils import setup_file_comparison_test, files_match


def test_multiple_files():
    output_a, expected_a = setup_file_comparison_test("test_multiple_files_a")
    output_b, expected_b = setup_file_comparison_test("test_multiple_files_b")
    subprocess.run(["python", "main.py", "--files", output_a, output_b])
    assert files_match(output_a, expected_a) and files_match(output_b, expected_b)


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
    assert "output.view.lkml:11: dimension 'b_dimension_name' missing label" in warnings
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
    assert "tests/test_files/test_check_required_params_param/output.view.lkml:11: dimension 'b_dimension_name' missing label sql hidden" in warnings
