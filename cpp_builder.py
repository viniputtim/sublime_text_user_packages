import argparse
import os
import platform
import sys


includes = ['include', os.path.join('..', 'include')]
test_folders = {'test', 'tests'}
source_folders = {'source', 'src'}


def to_snake(text):
    snake_text = text.lower()

    for char in [' ', '-']:
        snake_text = snake_text.replace(char, '_')

    return snake_text


def main():
    parser = argparse.ArgumentParser(description='Basic C++ project builder with attitude.')
    parser.add_argument('--path', required=True, help='Path to source file')
    parser.add_argument('--libs', default='', help='Comma-separated list of libraries to link (e.g. raylib)')
    parser.add_argument('--debug', default='on', help='Enable ("on") or disable ("off") debug mode')
    parser.add_argument('--version', default='c++23', help='C++ standard to use (e.g., c++17, gnu++20, c++23)')
    args = parser.parse_args()

    file_path = os.path.normpath(args.path)
    source_path = os.path.join(file_path, '..')
    source_path = os.path.abspath(source_path)
    libraries = args.libs.split(',') if args.libs else []
    debug_mode = args.debug
    cpp_version = args.version

    print(f'[INFO] debug_mode: {debug_mode}', flush=True)
    print(f'[INFO] cpp_version: {cpp_version}', flush=True)
    print(f'[INFO] file_path: {file_path}', flush=True)
    print(f'[INFO] source_path: {source_path}', flush=True)
    print(f'[INFO] libraries: {libraries}', flush=True)

    if not os.path.basename(source_path) in source_folders:
        print(
            '[ERROR] Wrong folder, genius. Try running it from "source" like an actual developer.',
            file=sys.stderr
        )
        sys.exit(1)

    project_path = os.path.abspath(os.path.join(source_path, '..'))

    project_name = os.path.basename(project_path)
    print(f'[INFO] project_name: {project_name}', flush=True)
    executable_name = to_snake(project_name)
    print(f'[INFO] executable_name: {executable_name}', flush=True)
    executable = os.path.join('..', 'bin', executable_name)
    output_folder = os.path.dirname(executable)
    output_folder = os.path.abspath(output_folder)
    print(f'[INFO] output_folder: {output_folder}', flush=True)

    os.makedirs(output_folder, exist_ok=True)

    include_flags = ' '.join(f'-I "{x}"' for x in includes)
    compile_flags = f'-std={cpp_version}' + (' -g' if debug_mode == 'on' else '')
    link_flags = ''

    if 'raylib' in libraries:
        if platform.system() == 'Windows':
            link_flags += ' -lraylib -lopengl32 -lgdi32 -lwinmm'
        else:
            link_flags += ' -lraylib -lGL -lm -lpthread -ldl -lrt -lX11'

    source_files = []

    for root, _, files in os.walk(source_path):
        root_parts = root.split(os.sep)

        if any(test_dir in root_parts for test_dir in test_folders):
            continue

        for file in files:
            if file.endswith(('.c', '.cpp', '.cxx')):
                source_files.append(os.path.join(root, file))

    print(f'[INFO] source_files: {source_files}')

    if not source_files:
        print('[ERROR] No source files found. Are you even trying?', file=sys.stderr)
        sys.exit(1)

    source_files_str = ' '.join(f'"{f}"' for f in source_files)
    command = f'g++ {compile_flags} -o "{executable}" {include_flags} {source_files_str} {link_flags}'
    print(f'[INFO] command: {command}', flush=True)

    if os.system('command -v g++ > /dev/null') != 0:
        print('[ERROR] Bro... you seriously trying to compile C++ without having g++ installed?', file=sys.stderr)
        sys.exit(1)

    if os.system(command) == 0:
        os.system(f'"{executable}"')
    else:
        print('[ERROR] Compilation failed. Maybe you should check your code? Just a thought.', file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
