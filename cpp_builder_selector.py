import os
import sys


packages_dir = '/home/vinicius/.config/sublime-text/Packages/User'


def main():
    if len(sys.argv) < 2:
        print('[ERROR] No arguments received. Either Sublime is bugging out or your build system is broken.', file=sys.stderr)
        sys.exit(1)

    if sys.argv[1].endswith('.h') or sys.argv[1].endswith('.hpp'):
        os.system(f'python3 "{packages_dir}/header_to_source.py" {sys.argv[1]}')
    else:
        os.system(f'python3 "{packages_dir}/cpp_builder.py" {" ".join(sys.argv[1:])}')


if __name__ == '__main__':
    main()
