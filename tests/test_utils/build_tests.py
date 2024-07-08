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
    with open("tests/test_utils/action_test_template.yml") as action_test_template:
        action_tests = action_test_template.read()
    
    for test_name, test_args in tests.items():
        generic_tests += f"""
        def {test_name}():
            output, expected = setup_file_comparison_test("{test_name}")
            subprocess.run(["python", "main.py", "--files", output, {" ,".join([f"\"{arg}\"" for arg in test_args])}])
            assert files_match(output, expected)
        """
        
        action_tests += f"""
            - name: Setup {test_name}
              shell: bash
              run: |
                cp tests/test_files/{test_name}/input.view.lkml tests/test_files/{test_name}/output.view.lkml
            - name: Run {test_name}
              uses: alhankeser/looker-janitor-action@latest
              with:
                files: |
                  tests/test_files/{test_name}/output.view.lkml"""
        for arg in test_args:
            if arg[0:2] == '--':
                action_tests += f"""
                {arg.replace("--","")}: |"""
            else:
                action_tests += f"""
                  {arg}"""
        action_tests += f"""
            - name: Compare output to expected
              shell: bash
              run: |
                if diff -s "tests/test_files/{test_name}/output.view.lkml" "tests/test_files/{test_name}/expected.view.lkml"; then
                  echo "{test_name} Passed"
                else
                  echo "::error:: {test_name} Failed"
                fi"""

    generic_tests = textwrap.dedent(generic_tests)
    with open("tests/test_generic.py", "w") as generic_tests_file:
        generic_tests_file.write(generic_tests)
    with open(".github/workflows/action_tests.yml", "w") as action_tests_file:
        action_tests_file.write(action_tests)


if __name__ == "__main__":
    main()