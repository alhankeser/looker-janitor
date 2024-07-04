import sys
import json
import textwrap

def main():
    with open(sys.argv[1]) as file_text:
        tests = json.load(file_text)
    generic_tests = """
        # this file is auto-generated 
        # run: tests/test_utils/build_tests.py tests/generic_tests.json

        import subprocess
        from test_utils import setup_file_comparison_test, files_match
        """

    for test_name, test_args in tests.items():
        generic_tests += f"""
        def {test_name}():
            output, expected = setup_file_comparison_test("{test_name}")
            subprocess.run(["python", "main.py", "--files", output, {" ,".join([f"\"{arg}\"" for arg in test_args])}])
            assert files_match(output, expected)
        """
    generic_tests = textwrap.dedent(generic_tests)
    with open("tests/generic_tests.py", "w") as output_file:
        output_file.write(generic_tests)

if __name__ == "__main__":
    main()