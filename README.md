# Sublime C++ Build System with Raylib Support



Custom C++ build system for Sublime Text, designed for multi-file projects and optional Raylib integration. Includes smart header-to-source code generation.

## 🚀 Features

- 🔢 Multi-file C++ project build support
- 🎮 Optional Raylib integration
- 📝 header_to_source.py: generates method stubs from `.h` / `.hpp` files
- 🐞 Debug mode toggle (`--debug=on|off`)
- 🧬 C++ standard selection (`--version=c++23|c++17|...`)
- 🧠 Smart file-type detection (header vs source)

## 🗂️ Project Structure

Expected folder layout:

### 📁project

- 📁 include: Header files (`.h` / `.hpp`)
- 📁 source: Source files (`.cpp`)
- 📁 bin: Output folder

## 🔨 Build Systems

Two build systems included:

### 🎮 C++ Raylib.sublime-build

```json
{
  "selector": "source.c, source.cpp, source.c++, source.h, source.hpp, source.h++",
  "shell_cmd": "python3 '/path/to/cpp_builder_selector.py' --path='$file_path' --libs='raylib' --version='gnu++23' --debug='on'"
}
```

### 🔢 C++ Multiple Files.sublime-build

```json
{
  "selector": "source.c, source.cpp, source.c++, source.h, source.hpp, source.h++",
  "shell_cmd": "python3 '/path/to/cpp_builder_selector.py' --path='$file_path' --version='gnu++23' --debug='on'"
}
```

## 🧠 How It Works

### ↔️ cpp_builder_selector.py

Routes build requests: if file is a header: runs `header_to_source.py` else runs `cpp_builder.py`

### 🔨 cpp_builder.py

Compiles all `.cpp` files inside 📁 *source*. Skips 📁 *tests* or 📁 *test* folders. Links `Raylib` if `--libs='raylib'` is set. Outputs binary to 📁 *bin* named after the project folder (in snake_case). Supports debug mode and C++ standard override.

### 📝 header_to_source.py

Parses header files. Generates stub implementations for all class methods. Maintains class scope (`ClassName::method()`).

## 🛠 Requirements

- g++ (compiler)
- python3
- Raylib installed (if using Raylib mode)

## ▶️ Usage

- Place scripts in your Sublime Packages/User/ directory.
- Open any file in your project.
- Hit Ctrl+B or Cmd+B to build — the system will handle the rest.

## 📄 License

MIT License. Free to use, fork, or contribute.
