# Helpers for cogging slides.

import textwrap

try:
    import cog
except ImportError:
    pass  # for running tests.

import cagedprompt
from edtext import EdText


def quote_html(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


INCLUDE_FILE_DEFAULTS = dict(
    fname=None,
    show_label=False,
    classes="",
    indir="",
)


def include_file_default(**kwargs):
    INCLUDE_FILE_DEFAULTS.update(kwargs)


def code(text, lang=None, highlight=None, px=False, classes=""):
    """Format text for a <pre> block."""

    text = textwrap.dedent(str(text))
    text_lines = text.splitlines()
    text = "\n".join(l.rstrip() for l in text_lines)

    if px:
        cog.outl(f"<code lang='{lang}'>")
        cog.outl(quote_html(text))
        cog.outl("</code>")
        return

    class_attr = lang or ""
    if classes:
        class_attr += " " + classes
    class_attr = " ".join(sorted(set(class_attr.split())))
    if class_attr:
        class_attr = f" class='{class_attr}'"

    hilite_attr = ""
    if highlight:
        hilite = []
        for h in highlight:
            if isinstance(h, int):
                hilite.append(h)
            else:
                hilite.extend(i for i, l in enumerate(text_lines) if h in l)

        hilite_attr = " data-hilite='|{}|'".format("|".join(map(str, hilite)))

    result = []
    result.append(f"<pre{class_attr}{hilite_attr}>")
    result.append(quote_html(text))
    result.append("</pre>")
    cog.outl("\n".join(result))


def prompt_session(input, command=False, prelude=""):
    output = ""
    if command:
        output += "$ python\n"
    repl_out = cagedprompt.prompt_session(input, banner=command, prelude=prelude)
    # REPL sessions have lone triple-dot lines. Suppress them.
    repl_out = "\n".join("" if l == "... " else l for l in repl_out.splitlines())
    output += repl_out
    code(output, lang="python", classes="console " + INCLUDE_FILE_DEFAULTS["classes"])


def include_file(filename: str) -> EdText:
    with open(filename) as f:
        return EdText(f.read())


def run_command(command: str, cwd: str | None = None) -> EdText:
    import subprocess

    output = f"$ {command}\n"
    result = subprocess.run(
        command,
        shell=True,
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
    )
    output += result.stdout
    if result.returncode != 0:
        output += f"(exit code: {result.returncode})\n"
    return EdText(output)
