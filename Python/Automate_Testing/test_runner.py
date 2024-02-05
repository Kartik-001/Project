import os
import ast
import shutil


def analyze_script(script_path):
    with open(script_path, 'r') as file:
        script_contents = file.read()

    # Parse the script using the AST parser
    tree = ast.parse(script_contents)

    function_names = []

    # Traverse the AST and identify functions
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            # Extract function name
            function_name = node.name
            function_names.append(function_name)

    return function_names


def generate_test_file(script_name, function_name):
    test_template = f"""
import pytest
import {script_name}


def test_{function_name}():
    # Test cases for {function_name}
    assert {script_name}.{function_name}(test_args) == expected_output
    assert {script_name}.{function_name}(test_args) == expected_output
    
    # Add more test cases...

"""
    add_on = f"    assert {script_name}.{function_name}(test_args) == expected_output"
    return test_template, add_on


def create_test_folder(script_path):
    script_name = os.path.splitext(os.path.basename(script_path))[0]
    test_folder = 'tests'
    test_folder_path = os.path.join(os.path.dirname(script_path), test_folder)

    # Create the tests folder if it doesn't exist
    if not os.path.exists(test_folder_path):
        os.makedirs(test_folder_path)

    # Copy the script to the tests folder
    shutil.copy2(script_path, test_folder_path)

    # Generate test files for each function
    function_names = analyze_script(script_path)
    for function_name in function_names:
        test_file_content, add_on = generate_test_file(script_name, function_name)
        test_file_path = os.path.join(test_folder_path, f'test_{function_name}.py')

        # Write the test file content
        if not os.path.exists(test_file_path):
            with open(test_file_path, 'w') as file:
                file.write(test_file_content)
        else:
            with open(test_file_path, "a") as file:
                file.write(add_on + "\n")

    # Create __init__.py file
    if not os.path.exists("tests/__init__.py"):
        init_file_path = os.path.join(test_folder_path, '__init__.py')
        with open(init_file_path, 'w'):
            pass

    print(f"Test folder created: {test_folder_path}")


if __name__ == '__main__':
    script_path = 'your_script.py'  # Replace with the path to your Python script
    create_test_folder(script_path)
