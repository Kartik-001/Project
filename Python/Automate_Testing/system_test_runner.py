import subprocess


def run_system_tests():
    system_test_cases = [
        {'command': 'python your_script.py 2 3', 'expected_output': '5\n6\n0.6666666666666666\n2\n'},
        {'command': 'python your_script.py 4 5', 'expected_output': '9\n20\n0.8\n24\n'},
        # Add more system test cases...
    ]

    for test_case in system_test_cases:
        command = test_case['command']
        expected_output = test_case['expected_output']
        result = subprocess.run(command, shell=True, capture_output=True, text=True)

        print(f'Running command: {command}')
        print('Expected output:')
        print(expected_output)
        print('Actual output:')
        print(result.stdout)
        print()

        if result.stdout.strip() == expected_output.strip():
            print('Test Passed')
        else:
            print('Test Failed')

        print('-' * 40)


if __name__ == '__main__':
    run_system_tests()
