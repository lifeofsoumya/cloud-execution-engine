import sys
import subprocess
import io

def execute_python_code(code):
    original_stdout = sys.stdout
    sys.stdout = output_capture = io.StringIO()
    try:
        exec(code)
        output = output_capture.getvalue()
        print('output of the code', output)
        return output
    except Exception as e:
        return str(e)
    finally:
        sys.stdout = original_stdout

def execute_java_code(code, timeout=5):
    try:
        with open('/tmp/temp.java', 'w') as java_file:
            java_file.write(code)
        compile_res = subprocess.run(
            ['javac', '/tmp/temp.java'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout
        )
        if compile_res.returncode != 0:
            return compile_res.stderr.decode()
        run_res = subprocess.run(
            ['java', '-classpath', '/tmp', 'temp'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout
        )

        return run_res.stdout.decode()

    except subprocess.TimeoutExpired:
        return "Execution timed out."
    except Exception as e:
        return "An error occurred: " + str(e)

# def execute_javascript_code(code):
#     try:
#         command = ['node', '-e', code]
#         result = subprocess.run(command, capture_output=True, text=True, check=True)
#         output = result.stdout.strip()
#         return output
#     except subprocess.CalledProcessError as e:
#         return str(e)
#     except subprocess.TimeoutExpired:
#         return "Execution timed out."
#     except Exception as e:
#         return str(e)

def execute_cpp_code(code):
    try:
        with open('/tmp/temp.cpp', 'w') as cpp_file:
            cpp_file.write(code)

        compile_res = subprocess.run(
            ['g++', '/tmp/temp.cpp', '-o', '/tmp/temp'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        print('compiled res', compile_res.returncode)
        if compile_res.returncode != 0:
            return compile_res.stderr.decode()
        run_res = subprocess.run(
            ['/tmp/temp'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        return run_res.stdout.decode()
    except subprocess.CalledProcessError as e:
        return str(e)
    except Exception as e:
        return "An error occurred: " + str(e)

def handler(event, context):
    code = event.get('code', '')
    language = event.get('language', 'python')
    if language == 'python':
        result = execute_python_code(code)
    elif language == 'cpp':
        result = execute_cpp_code(code)
    elif language == 'java':
        result = execute_java_code(code)
    else:
        result = 'Unsupported language ' + language
    return {
        'statusCode': 200,
        'body': result
    }

