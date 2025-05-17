import os
import sublime
import sublime_plugin


class MyFileOpenListener(sublime_plugin.EventListener):
    def on_load(self, view):
        file_path = view.file_name()
        file_name = os.path.basename(file_path)
        file_noext = os.path.splitext(file_name)[0]
        source_exts = ('.c', '.cpp', '.cxx')
        header_exts = ('.h', '.hpp', '.hxx')
        sources = ['source', 'src']
        includes = ['include', 'includes']
        dirs = file_path.split(os.sep)
        window = view.window()

        def _open_pair_file(root_folders, pair_folders, pair_exts):
            indexes = {x: dirs.index(x) for x in root_folders if x in dirs}
            match = max(indexes, key=indexes.get) if indexes else None
            match_index = indexes[match] if match else None
            project_path = os.sep.join(dirs[:match_index]) if match_index else None
            subdirs_path = os.sep.join(dirs[match_index + 1:-1]) if match_index else None

            if not project_path:
                return

            pair_paths = [os.path.join(project_path, folder) for folder in pair_folders]
            search_files = [f'{file_noext}{ext}' for ext in pair_exts]

            for pair_path in pair_paths:
                for search_file in search_files:
                    full_path = os.path.join(pair_path, subdirs_path, search_file)

                    if os.path.isfile(full_path):
                        window.open_file(full_path)
                        return

        if file_name.endswith(source_exts):
            _open_pair_file(sources, includes, header_exts)
        elif file_name.endswith(header_exts):
            _open_pair_file(includes, sources, source_exts)
