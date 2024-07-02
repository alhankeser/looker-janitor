import subprocess

TEST_FILE_DIR = "tests/test_files/"

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