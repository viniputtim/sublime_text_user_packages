import argparse
import http.server
import os
import socket
import socketserver
import sys
import webbrowser
import subprocess


port = 8000
resources = ['resource', 'resources']
includes = ['include', os.path.join('..', 'include')]
test_folders = {'test', 'tests'}
source_folders = {'source', 'src'}
emsdk_path = '/home/vinicius/Desenvolvimento/emsdk'
raylib_path = '/home/vinicius/Desenvolvimento/raylib/src'
raylib_web_a_path = os.path.join(raylib_path, 'libraylib.a')
raylib_min_shell_path = os.path.join(raylib_path, 'minshell.html')


def to_snake(text):
    snake_text = text.lower()

    for char in [' ', '-']:
        snake_text = snake_text.replace(char, '_')

    return snake_text


def activate_emscripten():
    print('[INFO] Activating Emscripten environment...', flush=True)
    command = f'source {emsdk_path}/emsdk_env.sh && env'
    proc = subprocess.Popen(['/bin/bash', '-c', command], stdout=subprocess.PIPE)
    output = proc.communicate()[0].decode('utf-8')

    for line in output.splitlines():
        if '=' in line:
            var, val = line.strip().split('=', 1)
            os.environ[var] = val


def tranform_to_absolute_paths(project_path):
    global includes
    global resources

    includes = [os.path.abspath(os.path.join(project_path, i)) for i in includes]
    resources = [
        os.path.abspath(os.path.join(project_path, i)) for i in resources if
        os.path.isdir(os.path.abspath(os.path.join(project_path, i)))
    ]


def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0


def main():
    parser = argparse.ArgumentParser(description='C++ Raylib Web Assembly builder.')
    parser.add_argument('--path', required=True, help='Path to source file.')
    parser.add_argument('--version', default='c++23', help='C++ standard to use.')
    args = parser.parse_args()

    activate_emscripten()

    file_path = os.path.normpath(args.path)
    source_path = os.path.join(file_path, '..')
    source_path = os.path.abspath(source_path)
    cpp_version = args.version

    print(f'[INFO] cpp_version: {cpp_version}', flush=True)
    print(f'[INFO] file_path: {file_path}', flush=True)
    print(f'[INFO] source_path: {source_path}', flush=True)

    if not os.path.basename(source_path) in source_folders:
        print('[ERROR] Wrong folder, genius. Try running it from "source" like an actual developer.', file=sys.stderr, flush=True)
        sys.exit(1)

    project_path = os.path.abspath(os.path.join(source_path, '..'))
    project_name = os.path.basename(project_path)
    print(f'[INFO] project_name: {project_name}', flush=True)
    executable_name = to_snake(project_name)
    print(f'[INFO] executable_name: {executable_name}', flush=True)
    executable = os.path.join('..', 'web', f'{executable_name}.html')
    output_folder = os.path.dirname(executable)
    output_folder = os.path.abspath(output_folder)
    print(f'[INFO] output_folder: {output_folder}', flush=True)

    os.makedirs(output_folder, exist_ok=True)
    tranform_to_absolute_paths(project_path);

    resource_flags =' '.join(f'--preload-file "{x}"' for x in resources)
    source_flags = f'-Os -Wall {raylib_web_a_path}'
    include_flags = ' '.join(f'-I "{x}"' for x in includes)
    include_flags = f'{include_flags} -I {raylib_path}'
    compile_flags = f'-std={cpp_version}'
    link_flags = f'-L {raylib_path}'
    config_flags = f'-s USE_GLFW=3 -s ASYNCIFY --shell-file {raylib_min_shell_path} -DPLATFORM_WEB'

    source_files = []

    for root, _, files in os.walk(source_path):
        root_parts = root.split(os.sep)

        if any(test_dir in root_parts for test_dir in test_folders):
            continue

        for file in files:
            if file.endswith(('.c', '.cpp', '.cxx')):
                source_files.append(os.path.join(root, file))

    print(f'[INFO] source_files: {source_files}', flush=True)

    if not source_files:
        print('[ERROR] No source files found. Are you even trying?', file=sys.stderr, flush=True)
        sys.exit(1)

    source_files_str = ' '.join(f'"{f}"' for f in source_files)
    command = f'emcc {compile_flags} -o "{executable}" {resource_flags} {source_files_str} {source_flags} {include_flags} {link_flags} {config_flags}'
    print(f'[INFO] command: {command}', flush=True)

    if os.system(command) == 0:
        if is_port_in_use(port):
            print(f'[INFO] Server already running on port {port}, opening browser...', flush=True)
            webbrowser.open(f'http://localhost:{port}/{executable_name}.html')
        else:
            os.chdir(output_folder)
            Handler = http.server.SimpleHTTPRequestHandler
            with socketserver.TCPServer(("", port), Handler) as httpd:
                webbrowser.open(f'http://localhost:{port}/{executable_name}.html')
                print(f'[INFO] Serving HTTP on port {port} (http://localhost:{port}/) ...', flush=True)
                httpd.serve_forever()
    else:
        print('[ERROR] Compilation failed. Maybe you should check your code? Just a thought.', file=sys.stderr, flush=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
