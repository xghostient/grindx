"""Code editor with auto-indent, line operations, clipboard, and Esc passthrough."""

import re
from pathlib import Path
from textual.widgets import TextArea
from textual.events import Key

from ..clipboard import copy_to_clipboard, paste_from_clipboard

# C++ highlight query — combined C base + C++ additions.
# C++ grammar (tree-sitter-cpp) extends C, so we need both.
_CPP_HIGHLIGHT_QUERY = """\
; C base highlights

(identifier) @variable

((identifier) @constant
 (#match? @constant "^[A-Z][A-Z_0-9]*$"))

(call_expression
  function: (identifier) @function)

(call_expression
  function: (field_expression
    field: (field_identifier) @function))

(function_declarator
  declarator: (identifier) @function)

(preproc_def
  name: (identifier) @constant)

(type_identifier) @type
(primitive_type) @type.builtin
(sized_type_specifier) @type.builtin
(field_identifier) @property

[
  "break" "case" "const" "continue" "default" "do" "else"
  "enum" "extern" "for" "goto" "if" "inline" "return"
  "sizeof" "static" "struct" "switch" "typedef" "union"
  "volatile" "while"
] @keyword

[
  "#define" "#elif" "#else" "#endif" "#if" "#ifdef"
  "#ifndef" "#include"
] @keyword

[
  "--" "-" "-=" "->" "!" "!=" "*" "*=" "/" "/="
  "&" "&&" "&=" "%" "%=" "^" "^=" "+" "++" "+="
  "<" "<<" "<<=" "<=" "=" "==" ">" ">=" ">>" ">>="
  "|" "||" "|=" "~"
] @operator

(number_literal) @number
(char_literal) @string
(string_literal) @string
(system_lib_string) @string
(true) @constant.builtin
(false) @constant.builtin
(null) @constant.builtin
(comment) @comment

; C++ additions

(call_expression
  function: (qualified_identifier
    name: (identifier) @function))

(template_function
  name: (identifier) @function)

(template_method
  name: (field_identifier) @function)

(function_declarator
  declarator: (qualified_identifier
    name: (identifier) @function))

(function_declarator
  declarator: (field_identifier) @function)

((namespace_identifier) @type
 (#match? @type "^[A-Z]"))

(auto) @type

(this) @variable.builtin
(null "nullptr" @constant)

[
  "catch" "class" "co_await" "co_return" "co_yield"
  "constexpr" "constinit" "consteval" "delete" "explicit"
  "final" "friend" "mutable" "namespace" "noexcept" "new"
  "override" "private" "protected" "public" "template"
  "throw" "try" "typename" "using" "concept" "requires" "virtual"
] @keyword

(raw_string_literal) @string
"""

# Keys that the editor should NOT handle — route to screen actions instead
_PASSTHROUGH = {
    "ctrl+d": "mark_done",
    "ctrl+b": "toggle_bookmark",
    "ctrl+t": "toggle_timer",
    "ctrl+r": "reset_timer",
    "ctrl+l": "toggle_lang",
    "ctrl+e": "evaluate",
}


class CodeEditor(TextArea):

    def on_mount(self) -> None:
        """Register C++ language (not a Textual built-in)."""
        try:
            from textual._tree_sitter import get_language
            cpp_lang = get_language("cpp")
            if cpp_lang is not None:
                self.register_language("cpp", cpp_lang, _CPP_HIGHLIGHT_QUERY)
                # Re-apply if editor was created with language="cpp" before registration
                if self.language == "cpp":
                    self.language = None
                    self.language = "cpp"
        except Exception:
            pass

    def _on_key(self, event: Key) -> None:
        if event.key == "escape":
            event.stop()
            event.prevent_default()
            self.screen.action_go_back()
            return

        if event.key in _PASSTHROUGH:
            event.stop()
            event.prevent_default()
            action = _PASSTHROUGH[event.key]
            if hasattr(self.screen, f"action_{action}"):
                getattr(self.screen, f"action_{action}")()
            return

        # Clipboard: Ctrl+Shift+C to copy, Ctrl+Shift+V to paste
        if event.key == "ctrl+shift+c":
            event.stop()
            event.prevent_default()
            self._copy_selection()
            return

        if event.key == "ctrl+shift+v":
            event.stop()
            event.prevent_default()
            self._paste_clipboard()
            return

        # Alt+Up/Down: move line, Alt+Shift+Down: duplicate line
        if event.key == "alt+up":
            event.stop()
            event.prevent_default()
            self._move_line(-1)
            return

        if event.key == "alt+down":
            event.stop()
            event.prevent_default()
            self._move_line(1)
            return

        if event.key == "alt+shift+down":
            event.stop()
            event.prevent_default()
            self._duplicate_line()
            return

        if event.key == "enter":
            row, col = self.cursor_location
            current_line = self.document.get_line(row)
            indent = re.match(r"^(\s*)", current_line).group(1)
            text_before_cursor = current_line[:col].rstrip()
            if text_before_cursor.endswith(":") or text_before_cursor.endswith("{"):
                indent += "    "
            event.stop()
            event.prevent_default()
            self.insert("\n" + indent)
            return

        super()._on_key(event)

    # ─── Clipboard ───

    def _copy_selection(self) -> None:
        """Copy selected text to system clipboard."""
        text = self.selected_text
        if text:
            copy_to_clipboard(text)

    def _paste_clipboard(self) -> None:
        """Paste from system clipboard at cursor."""
        text = paste_from_clipboard()
        if text:
            self.insert(text)

    # ─── Line operations ───

    def _move_line(self, direction: int) -> None:
        """Move current line up (-1) or down (+1)."""
        row, col = self.cursor_location
        line_count = self.document.line_count
        target = row + direction
        if target < 0 or target >= line_count:
            return
        lines = self.text.split("\n")
        lines[row], lines[target] = lines[target], lines[row]
        self.text = "\n".join(lines)
        self.cursor_location = (target, col)

    def _duplicate_line(self) -> None:
        """Duplicate current line below."""
        row, col = self.cursor_location
        lines = self.text.split("\n")
        lines.insert(row + 1, lines[row])
        self.text = "\n".join(lines)
        self.cursor_location = (row + 1, col)
