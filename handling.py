"""
╔══════════════════════════════════════════════════════════════════════╗
║   Python FILE HANDLING – Complete Streamlit Reference App            ║
║   All Methods · All Functions · 100 Code Examples                    ║
║   Run:  streamlit run streamlit_file_handling.py                     ║
╚══════════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import os, io, sys, shutil, json, csv, tempfile, pathlib, stat
import contextlib, textwrap, traceback, random, time, re
from pathlib import Path
from datetime import datetime

# ──────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ──────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Python File Handling – Complete Reference",
    page_icon="📂",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────────────────────────────
# GLOBAL SANDBOX DIR  (all playground writes go here)
# ──────────────────────────────────────────────────────────────────────
SANDBOX = Path(tempfile.mkdtemp(prefix="fh_sandbox_"))

# ──────────────────────────────────────────────────────────────────────
# CSS
# ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
html,body,[class*="css"]{font-family:'Segoe UI',sans-serif;}
.main .block-container{padding-top:1rem;padding-bottom:2rem;}

.hero{
  background:linear-gradient(135deg,#0a0a1a 0%,#0d2137 50%,#0a3d2e 100%);
  border-radius:16px;padding:2.5rem 2rem 2rem;margin-bottom:1.5rem;
  text-align:center;box-shadow:0 8px 32px rgba(0,0,0,.4);
}
.hero h1{color:#00d4aa;font-size:2.6rem;margin:0;}
.hero p {color:#a8dadc;font-size:1.1rem;margin-top:.5rem;}

.sec-header{
  background:linear-gradient(90deg,#00d4aa,#0a3d2e);
  color:white;padding:.55rem 1.2rem;border-radius:8px;
  font-size:1.15rem;font-weight:700;margin:1.2rem 0 .8rem;
}

.card{
  background:#0d1f1a;border:1px solid #1a3a2a;
  border-left:4px solid #00d4aa;border-radius:10px;
  padding:1rem 1.2rem .7rem;margin-bottom:1rem;
  box-shadow:0 2px 8px rgba(0,0,0,.25);
}
.card-title{color:#00d4aa;font-size:1.05rem;font-weight:700;margin-bottom:.25rem;}
.card-def  {color:#a8dadc;font-size:.88rem;margin-bottom:.6rem;font-style:italic;}
.card-syntax{
  background:#060f0c;color:#c9d1d9;border-radius:6px;
  padding:.5rem .8rem;font-family:'Courier New',monospace;font-size:.83rem;
  border-left:3px solid #58a6ff;white-space:pre-wrap;
}

.badge-beg{background:#1b5e20;color:white;padding:2px 8px;border-radius:12px;font-size:.78rem;font-weight:700;}
.badge-int{background:#0d47a1;color:white;padding:2px 8px;border-radius:12px;font-size:.78rem;font-weight:700;}
.badge-adv{background:#4a148c;color:white;padding:2px 8px;border-radius:12px;font-size:.78rem;font-weight:700;}

.stat-row{display:flex;gap:1rem;margin-bottom:1.2rem;flex-wrap:wrap;}
.stat-box{flex:1;min-width:120px;background:#0d1f1a;border:1px solid #1a3a2a;
  border-radius:10px;padding:.8rem 1rem;text-align:center;}
.stat-num{font-size:1.8rem;font-weight:800;color:#00d4aa;}
.stat-lbl{color:#8b949e;font-size:.78rem;}

.out-box{
  background:#060f0c;color:#00d4aa;border-radius:8px;
  padding:.7rem 1rem;font-family:'Courier New',monospace;font-size:.85rem;
  margin-top:.5rem;border:1px solid #1a3a2a;white-space:pre-wrap;
}

section[data-testid="stSidebar"]{background:#060f0c !important;}
section[data-testid="stSidebar"] *{color:#c9d1d9 !important;}
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────
# DATA  ── FILE OBJECT METHODS
# ──────────────────────────────────────────────────────────────────────
FILE_METHODS = [
    {
        "name": "read(size=-1)",
        "syntax": "file.read(size=-1)",
        "definition": "Read and return up to `size` bytes/characters. If size is omitted or -1, reads the entire file. Returns a str (text mode) or bytes (binary mode).",
        "example": 'with open("f.txt","w") as f: f.write("Hello World")\nwith open("f.txt") as f:\n    print(f.read())     # Hello World\n    # cursor is now at EOF\nwith open("f.txt") as f:\n    print(f.read(5))    # Hello',
        "tip": "After read(), the file cursor is at EOF. Call seek(0) to re-read.",
    },
    {
        "name": "readline(size=-1)",
        "syntax": "file.readline(size=-1)",
        "definition": "Read one complete line including the trailing newline. If size is given, reads at most that many characters. Returns '' at EOF.",
        "example": 'with open("f.txt","w") as f: f.write("line1\\nline2\\nline3")\nwith open("f.txt") as f:\n    print(repr(f.readline()))  # "line1\\n"\n    print(repr(f.readline()))  # "line2\\n"',
        "tip": "Use readline() for streaming large files line by line without loading everything.",
    },
    {
        "name": "readlines(hint=-1)",
        "syntax": "file.readlines(hint=-1)",
        "definition": "Read all lines and return a list of strings, each ending with '\\n'. hint limits total bytes read.",
        "example": 'with open("f.txt") as f:\n    lines = f.readlines()\nprint(lines)  # ["line1\\n","line2\\n","line3"]',
        "tip": "For big files prefer iterating: 'for line in file' is memory-efficient.",
    },
    {
        "name": "write(s)",
        "syntax": "file.write(s)",
        "definition": "Write string s (text mode) or bytes b (binary mode) to the file. Returns the number of characters/bytes written.",
        "example": 'with open("out.txt","w") as f:\n    n = f.write("Hello, File!")\n    print(n)  # 12',
        "tip": "write() does NOT add a newline. Use '\\n' explicitly or writelines().",
    },
    {
        "name": "writelines(lines)",
        "syntax": "file.writelines(iterable)",
        "definition": "Write an iterable of strings (or bytes) to the file. Does NOT add newlines between items.",
        "example": 'lines = ["one\\n","two\\n","three\\n"]\nwith open("out.txt","w") as f:\n    f.writelines(lines)',
        "tip": "You must include '\\n' in each string yourself.",
    },
    {
        "name": "seek(offset, whence=0)",
        "syntax": "file.seek(offset, whence=0)",
        "definition": "Move the cursor to offset bytes. whence: 0=start, 1=current, 2=end. Returns new position.",
        "example": 'with open("f.txt","rb") as f:\n    f.seek(0, 2)        # move to end\n    size = f.tell()     # file size\n    f.seek(0)           # back to start\n    print(size)',
        "tip": "seek() with whence=1 or 2 requires binary mode on some platforms.",
    },
    {
        "name": "tell()",
        "syntax": "file.tell()",
        "definition": "Return the current position of the file cursor (number of bytes from start).",
        "example": 'with open("f.txt") as f:\n    f.read(5)\n    print(f.tell())  # 5',
        "tip": "Use tell() to save a position, then seek() back to it later.",
    },
    {
        "name": "flush()",
        "syntax": "file.flush()",
        "definition": "Flush the internal write buffer to the OS. Data is written to disk without closing the file.",
        "example": 'with open("log.txt","w") as f:\n    f.write("start\\n")\n    f.flush()   # force write to disk now\n    # ... more work ...\n    f.write("end\\n")',
        "tip": "Useful in long-running processes (loggers, progress writers) to avoid data loss.",
    },
    {
        "name": "close()",
        "syntax": "file.close()",
        "definition": "Flush and close the file. After close(), any operation on the file raises ValueError.",
        "example": 'f = open("f.txt","w")\nf.write("data")\nf.close()\nprint(f.closed)  # True',
        "tip": "Always prefer 'with open(...)' — it calls close() automatically even on exceptions.",
    },
    {
        "name": "truncate(size=None)",
        "syntax": "file.truncate(size=None)",
        "definition": "Resize the file to at most size bytes. If size is omitted, truncate at current position.",
        "example": 'with open("f.txt","w") as f: f.write("Hello World")\nwith open("f.txt","r+") as f:\n    f.truncate(5)\nwith open("f.txt") as f:\n    print(f.read())  # Hello',
        "tip": "Open in 'r+' or 'w' mode before truncating.",
    },
    {
        "name": "fileno()",
        "syntax": "file.fileno()",
        "definition": "Return the integer file descriptor used by the OS for this file object.",
        "example": 'with open("f.txt","w") as f:\n    fd = f.fileno()\n    print(fd)  # e.g., 3',
        "tip": "Used for low-level OS calls like os.fstat(fd) or os.sendfile().",
    },
    {
        "name": "isatty()",
        "syntax": "file.isatty()",
        "definition": "Return True if the file is connected to a terminal (tty). False for regular files.",
        "example": 'with open("f.txt") as f:\n    print(f.isatty())   # False\nprint(sys.stdin.isatty())  # True if interactive',
        "tip": "Use isatty() to detect if output goes to a terminal vs a pipe/file.",
    },
    {
        "name": "readable()",
        "syntax": "file.readable()",
        "definition": "Return True if the file can be read (opened in 'r', 'r+', 'rb', etc.).",
        "example": 'with open("f.txt","w") as f:\n    print(f.readable())   # False\nwith open("f.txt","r") as f:\n    print(f.readable())   # True',
        "tip": "Check before calling read() if the file mode is dynamic.",
    },
    {
        "name": "writable()",
        "syntax": "file.writable()",
        "definition": "Return True if the file can be written to (opened in 'w', 'a', 'r+', etc.).",
        "example": 'with open("f.txt","r") as f:\n    print(f.writable())   # False\nwith open("f.txt","w") as f:\n    print(f.writable())   # True',
        "tip": "Prevents accidental writes to read-only files at runtime.",
    },
    {
        "name": "seekable()",
        "syntax": "file.seekable()",
        "definition": "Return True if the file supports random access (seek/tell). Pipes and sockets return False.",
        "example": 'with open("f.txt","r") as f:\n    print(f.seekable())  # True\nprint(sys.stdin.seekable())  # False',
        "tip": "Always check seekable() before calling seek() on unknown file objects.",
    },
]

# ──────────────────────────────────────────────────────────────────────
# DATA  ── OPEN() MODES + OS / PATHLIB FUNCTIONS
# ──────────────────────────────────────────────────────────────────────
OPEN_MODES = [
    ("r",   "Read text (default). Error if file doesn't exist."),
    ("w",   "Write text. Creates or OVERWRITES the file."),
    ("a",   "Append text. Creates if not exists; never truncates."),
    ("x",   "Exclusive creation. Fails if file already exists."),
    ("r+",  "Read + Write text. File must exist. Cursor at start."),
    ("w+",  "Read + Write text. Creates or overwrites."),
    ("a+",  "Read + Append text. Creates if not exists."),
    ("rb",  "Read binary. Returns bytes."),
    ("wb",  "Write binary. Creates or overwrites."),
    ("ab",  "Append binary."),
    ("rb+", "Read + Write binary."),
    ("wb+", "Read + Write binary. Creates or overwrites."),
]

OS_FUNCTIONS = [
    ("os.getcwd()",               "Return current working directory path."),
    ("os.chdir(path)",            "Change the current working directory."),
    ("os.listdir(path='.')",      "Return list of names in directory."),
    ("os.mkdir(path)",            "Create a single directory."),
    ("os.makedirs(path)",         "Create directories recursively (like mkdir -p)."),
    ("os.remove(path)",           "Delete a file. Error if it doesn't exist."),
    ("os.unlink(path)",           "Alias for os.remove()."),
    ("os.rmdir(path)",            "Remove an EMPTY directory."),
    ("os.rename(src, dst)",       "Rename/move a file or directory."),
    ("os.replace(src, dst)",      "Rename; overwrites dst if it exists."),
    ("os.path.exists(path)",      "Return True if path exists (file or dir)."),
    ("os.path.isfile(path)",      "Return True if path is a regular file."),
    ("os.path.isdir(path)",       "Return True if path is a directory."),
    ("os.path.join(*parts)",      "Join path components with OS separator."),
    ("os.path.split(path)",       "Split into (head, tail) — dir and filename."),
    ("os.path.splitext(path)",    "Split into (root, ext) e.g. ('f', '.txt')."),
    ("os.path.basename(path)",    "Return the final component of a path."),
    ("os.path.dirname(path)",     "Return the directory component."),
    ("os.path.getsize(path)",     "Return file size in bytes."),
    ("os.path.abspath(path)",     "Return absolute path."),
    ("os.stat(path)",             "Return os.stat_result with file metadata."),
    ("os.walk(top)",              "Generate (dirpath, dirnames, filenames) tuples."),
    ("shutil.copy(src, dst)",     "Copy file content and permissions."),
    ("shutil.copy2(src, dst)",    "Copy file + metadata (timestamps)."),
    ("shutil.move(src, dst)",     "Move/rename file or directory."),
    ("shutil.rmtree(path)",       "Recursively delete a directory tree."),
    ("shutil.make_archive(...)",  "Create zip/tar archive of a directory."),
]

PATHLIB_METHODS = [
    ("Path(path)",            "Create a Path object."),
    ("Path.cwd()",            "Return current working directory as Path."),
    ("Path.home()",           "Return user's home directory as Path."),
    ("p / 'subdir'",          "Join path components with / operator."),
    ("p.exists()",            "True if path exists."),
    ("p.is_file()",           "True if path is a regular file."),
    ("p.is_dir()",            "True if path is a directory."),
    ("p.read_text()",         "Read entire file as string."),
    ("p.write_text(s)",       "Write string s to file (overwrites)."),
    ("p.read_bytes()",        "Read file as bytes object."),
    ("p.write_bytes(b)",      "Write bytes to file (overwrites)."),
    ("p.open(mode)",          "Open the file (like built-in open())."),
    ("p.mkdir(parents=True)", "Create directory (and parents)."),
    ("p.unlink()",            "Delete the file."),
    ("p.rmdir()",             "Remove empty directory."),
    ("p.rename(target)",      "Rename/move the path."),
    ("p.stat()",              "Return stat_result for the path."),
    ("p.iterdir()",           "Iterate over directory contents."),
    ("p.glob(pattern)",       "Glob matching files in directory."),
    ("p.rglob(pattern)",      "Recursive glob (searches subdirs)."),
    ("p.parent",              "The parent directory as a Path."),
    ("p.name",                "Final path component (filename)."),
    ("p.stem",                "Filename without extension."),
    ("p.suffix",              "File extension e.g. '.txt'."),
    ("p.suffixes",            "List of all extensions e.g. ['.tar','.gz']."),
    ("p.resolve()",           "Absolute path with symlinks resolved."),
    ("p.with_suffix('.csv')", "Return new path with different extension."),
    ("p.with_name('b.txt')",  "Return new path with different filename."),
]

# ──────────────────────────────────────────────────────────────────────
# 100 EXAMPLES
# ──────────────────────────────────────────────────────────────────────
EXAMPLES = [
    # ── BEGINNER 1–30 ──
    (1,"Create and write a text file","Beginner",
     "open() with 'w' mode creates the file (or overwrites) and write() stores content.",
     """import tempfile, os
path = os.path.join(tempfile.gettempdir(), "hello.txt")

with open(path, "w") as f:
    f.write("Hello, File Handling!\\n")
    f.write("Second line here.\\n")

print("File created:", path)
"""),

    (2,"Read an entire file","Beginner",
     "open() with 'r' (default) + read() loads the whole content as one string.",
     """import tempfile, os
path = os.path.join(tempfile.gettempdir(), "demo.txt")
with open(path,"w") as f: f.write("Line 1\\nLine 2\\nLine 3\\n")

with open(path, "r") as f:
    content = f.read()

print(content)
print("Characters:", len(content))
"""),

    (3,"Read file line by line (for loop)","Beginner",
     "Iterating a file object yields one line at a time — memory-efficient for large files.",
     """import tempfile, os
path = os.path.join(tempfile.gettempdir(), "lines.txt")
with open(path,"w") as f:
    f.writelines([f"Item {i}\\n" for i in range(1,6)])

with open(path) as f:
    for i, line in enumerate(f, 1):
        print(f"Line {i}: {line.rstrip()}")
"""),

    (4,"readline() — one line at a time","Beginner",
     "readline() advances the cursor by exactly one line on each call.",
     """import tempfile, os
path = os.path.join(tempfile.gettempdir(), "rl.txt")
with open(path,"w") as f: f.write("alpha\\nbeta\\ngamma\\n")

with open(path) as f:
    print(repr(f.readline()))   # 'alpha\\n'
    print(repr(f.readline()))   # 'beta\\n'
    print(repr(f.readline()))   # 'gamma\\n'
    print(repr(f.readline()))   # ''  ← EOF
"""),

    (5,"readlines() — all lines as list","Beginner",
     "readlines() returns a list of strings, one per line including the newline character.",
     """import tempfile, os
path = os.path.join(tempfile.gettempdir(), "rls.txt")
with open(path,"w") as f: f.write("one\\ntwo\\nthree\\n")

with open(path) as f:
    lines = f.readlines()

print(lines)
print("Total lines:", len(lines))
print("Stripped:", [l.strip() for l in lines])
"""),

    (6,"Append to an existing file","Beginner",
     "'a' mode moves the cursor to EOF before every write — never truncates existing content.",
     """import tempfile, os
path = os.path.join(tempfile.gettempdir(), "log.txt")
# Create
with open(path,"w") as f: f.write("Entry 1\\n")
# Append twice
with open(path,"a") as f: f.write("Entry 2\\n")
with open(path,"a") as f: f.write("Entry 3\\n")

with open(path) as f: print(f.read())
"""),

    (7,"Check if file exists before reading","Beginner",
     "os.path.exists() prevents FileNotFoundError when the file may be absent.",
     """import os, tempfile

path = os.path.join(tempfile.gettempdir(), "maybe.txt")

if os.path.exists(path):
    with open(path) as f:
        print(f.read())
else:
    print(f"File does not exist: {path}")
    # Create it
    with open(path,"w") as f:
        f.write("Created now!\\n")
    print("File created.")
"""),

    (8,"Write and read binary file","Beginner",
     "'wb' writes raw bytes; 'rb' reads them back. Use for images, PDFs, executables.",
     """import tempfile, os
path = os.path.join(tempfile.gettempdir(), "data.bin")

data = bytes(range(16))          # b'\\x00\\x01...\\x0f'
with open(path,"wb") as f:
    f.write(data)

with open(path,"rb") as f:
    back = f.read()

print("Written:", data.hex())
print("Read back:", back.hex())
print("Match:", data == back)
"""),

    (9,"tell() and seek() — cursor control","Beginner",
     "tell() returns current position; seek(n) jumps to byte offset n from start.",
     """import tempfile, os
path = os.path.join(tempfile.gettempdir(), "seek.txt")
with open(path,"w") as f: f.write("ABCDEFGHIJ")

with open(path,"r") as f:
    print(f.read(3))     # ABC  (pos → 3)
    print(f.tell())      # 3
    f.seek(7)
    print(f.read())      # HIJ
    f.seek(0)
    print(f.read(5))     # ABCDE
"""),

    (10,"with statement — context manager","Beginner",
     "The 'with' block guarantees the file is closed even if an exception occurs.",
     """import tempfile, os
path = os.path.join(tempfile.gettempdir(), "ctx.txt")

with open(path,"w") as f:
    f.write("context manager demo")
    print("File open inside with:", not f.closed)

print("File closed after with:", f.closed)
"""),

    (11,"writelines() — write list of strings","Beginner",
     "writelines() accepts any iterable of strings. No newlines are added automatically.",
     """import tempfile, os
path = os.path.join(tempfile.gettempdir(), "wl.txt")
lines = ["Python\\n", "File\\n", "Handling\\n"]

with open(path,"w") as f:
    f.writelines(lines)

with open(path) as f:
    print(f.read())
"""),

    (12,"File properties (name, mode, closed)","Beginner",
     "File objects expose .name, .mode, .closed as attributes.",
     """import tempfile, os
path = os.path.join(tempfile.gettempdir(), "props.txt")
with open(path,"w") as f: f.write("x")

with open(path,"r") as f:
    print("Name  :", f.name)
    print("Mode  :", f.mode)
    print("Closed:", f.closed)

print("After with, closed:", f.closed)
"""),

    (13,"os.path — file info","Beginner",
     "os.path functions inspect paths without opening the file.",
     """import os, tempfile
path = os.path.join(tempfile.gettempdir(), "info.txt")
with open(path,"w") as f: f.write("Hello!")

print("Exists  :", os.path.exists(path))
print("Is file :", os.path.isfile(path))
print("Is dir  :", os.path.isdir(path))
print("Size    :", os.path.getsize(path), "bytes")
print("Dirname :", os.path.dirname(path))
print("Basename:", os.path.basename(path))
print("Splitext:", os.path.splitext(path))
"""),

    (14,"Create and list a directory","Beginner",
     "os.makedirs creates nested directories; os.listdir lists their contents.",
     """import os, tempfile
base = os.path.join(tempfile.gettempdir(), "demo_dir")
os.makedirs(base, exist_ok=True)

# Create some files
for name in ["a.txt","b.txt","c.py"]:
    with open(os.path.join(base,name),"w") as f:
        f.write(name)

print("Contents of", base)
for item in os.listdir(base):
    print(" -", item)
"""),

    (15,"Delete a file","Beginner",
     "os.remove() deletes a file. Always check existence first to avoid errors.",
     """import os, tempfile
path = os.path.join(tempfile.gettempdir(), "todelete.txt")
with open(path,"w") as f: f.write("bye")

print("Before:", os.path.exists(path))
os.remove(path)
print("After:", os.path.exists(path))

# Safe delete
def safe_delete(p):
    if os.path.exists(p):
        os.remove(p); print(f"Deleted {p}")
    else:
        print(f"Not found: {p}")

safe_delete(path)   # already gone
"""),

    (16,"Rename and move a file","Beginner",
     "os.rename() renames in place; shutil.move() moves across directories.",
     """import os, shutil, tempfile
d = tempfile.gettempdir()
src = os.path.join(d,"old.txt")
dst = os.path.join(d,"new.txt")

with open(src,"w") as f: f.write("rename me")
print("Before:", os.path.exists(src), os.path.exists(dst))

os.rename(src, dst)
print("After rename:", os.path.exists(src), os.path.exists(dst))

# Move using shutil
dst2 = os.path.join(d,"moved.txt")
shutil.move(dst, dst2)
print("After move:", os.path.exists(dst), os.path.exists(dst2))
"""),

    (17,"Copy a file with shutil","Beginner",
     "shutil.copy() copies content+permissions; shutil.copy2() preserves timestamps too.",
     """import shutil, tempfile, os
d = tempfile.gettempdir()
src = os.path.join(d,"original.txt")
dst = os.path.join(d,"copy.txt")

with open(src,"w") as f: f.write("original content")
shutil.copy(src, dst)

with open(dst) as f:
    print("Copy content:", f.read())

print("Both exist:", os.path.exists(src), os.path.exists(dst))
"""),

    (18,"Read file into a list of stripped lines","Beginner",
     "Strip whitespace and filter blank lines while reading.",
     """import tempfile, os
path = os.path.join(tempfile.gettempdir(), "strip.txt")
with open(path,"w") as f:
    f.write("  apple  \\n\\n  banana  \\n  cherry  \\n\\n")

with open(path) as f:
    lines = [l.strip() for l in f if l.strip()]

print(lines)
print("Non-empty lines:", len(lines))
"""),

    (19,"Count words and lines in a file","Beginner",
     "Iterate lines to count them; split each line to count words.",
     """import tempfile, os
path = os.path.join(tempfile.gettempdir(), "count.txt")
with open(path,"w") as f:
    f.write("the quick brown fox\\njumps over the lazy dog\\n")

line_count = word_count = char_count = 0
with open(path) as f:
    for line in f:
        line_count += 1
        word_count += len(line.split())
        char_count += len(line)

print(f"Lines: {line_count}, Words: {word_count}, Chars: {char_count}")
"""),

    (20,"Handle FileNotFoundError","Beginner",
     "Wrap file operations in try/except to handle missing files gracefully.",
     """try:
    with open("/nonexistent/path/file.txt") as f:
        print(f.read())
except FileNotFoundError as e:
    print(f"File not found: {e}")
except PermissionError as e:
    print(f"Permission denied: {e}")
except IOError as e:
    print(f"IO Error: {e}")
finally:
    print("Done — cleanup can go here")
"""),

    (21,"Get file size","Beginner",
     "os.path.getsize() returns size in bytes without opening the file.",
     """import os, tempfile
path = os.path.join(tempfile.gettempdir(), "size.txt")
with open(path,"w") as f:
    f.write("A" * 1024)   # 1 KB

size = os.path.getsize(path)
print(f"Size: {size} bytes")
print(f"Size: {size/1024:.2f} KB")
"""),

    (22,"Read file in chunks","Beginner",
     "Read large files in fixed-size chunks to keep memory usage low.",
     """import tempfile, os
path = os.path.join(tempfile.gettempdir(), "chunk.txt")
with open(path,"w") as f: f.write("A" * 200)

chunk_size = 50
chunks = []
with open(path) as f:
    while True:
        chunk = f.read(chunk_size)
        if not chunk:
            break
        chunks.append(chunk)

print(f"Read {len(chunks)} chunks of {chunk_size} chars")
print("Total chars:", sum(len(c) for c in chunks))
"""),

    (23,"Truncate a file","Beginner",
     "truncate(n) shrinks the file to n bytes. Open in 'r+' to preserve existing content.",
     """import tempfile, os
path = os.path.join(tempfile.gettempdir(), "trunc.txt")
with open(path,"w") as f: f.write("Hello, World!")

with open(path,"r+") as f:
    f.truncate(5)

with open(path) as f:
    print(repr(f.read()))   # 'Hello'
"""),

    (24,"flush() — force write to disk","Beginner",
     "flush() writes buffered data to the OS without closing the file.",
     """import tempfile, os, time
path = os.path.join(tempfile.gettempdir(), "flush.txt")

with open(path,"w") as f:
    f.write("start\\n")
    f.flush()               # guaranteed on disk now
    time.sleep(0)           # simulate work
    f.write("end\\n")

with open(path) as f:
    print(f.read())
"""),

    (25,"readable(), writable(), seekable()","Beginner",
     "These boolean methods check file capabilities before performing operations.",
     """import tempfile, os
path = os.path.join(tempfile.gettempdir(), "caps.txt")
with open(path,"w") as f: f.write("data")

with open(path,"r") as f:
    print("Mode r — readable:", f.readable(),
          "writable:", f.writable(), "seekable:", f.seekable())

with open(path,"w") as f:
    print("Mode w — readable:", f.readable(),
          "writable:", f.writable(), "seekable:", f.seekable())

with open(path,"r+") as f:
    print("Mode r+ — readable:", f.readable(),
          "writable:", f.writable(), "seekable:", f.seekable())
"""),

    (26,"os.path.join — safe path building","Beginner",
     "os.path.join() uses the correct separator for the OS (/ on Unix, \\ on Windows).",
     """import os
home = os.path.expanduser("~")
docs = os.path.join(home, "Documents", "project", "notes.txt")
print("Joined path:", docs)
print("Basename:", os.path.basename(docs))
print("Extension:", os.path.splitext(docs)[1])
print("Abs path:", os.path.abspath("./relative.txt"))
"""),

    (27,"List directory with os.listdir","Beginner",
     "os.listdir() returns file and folder names; filter with isfile/isdir.",
     """import os, tempfile
d = tempfile.gettempdir()
print("Files in temp dir (first 10):")
items = os.listdir(d)[:10]
for item in items:
    full = os.path.join(d, item)
    kind = "DIR " if os.path.isdir(full) else "FILE"
    size = os.path.getsize(full) if os.path.isfile(full) else "-"
    print(f"  [{kind}] {item}  ({size})")
"""),

    (28,"Read and write with encoding","Beginner",
     "Always specify encoding (usually 'utf-8') to handle non-ASCII text correctly.",
     """import tempfile, os
path = os.path.join(tempfile.gettempdir(), "unicode.txt")

text = "Hello 🌍  Привет  日本語  العربية"
with open(path,"w", encoding="utf-8") as f:
    f.write(text)

with open(path,"r", encoding="utf-8") as f:
    back = f.read()

print(back)
print("Match:", text == back)
"""),

    (29,"pathlib.Path basics","Beginner",
     "pathlib.Path is the modern OOP way to work with paths — readable and cross-platform.",
     """from pathlib import Path
import tempfile

p = Path(tempfile.gettempdir()) / "pathlib_demo.txt"
p.write_text("Pathlib is great!")
print("Content:", p.read_text())
print("Name   :", p.name)
print("Stem   :", p.stem)
print("Suffix :", p.suffix)
print("Parent :", p.parent)
print("Exists :", p.exists())
p.unlink()
print("After unlink:", p.exists())
"""),

    (30,"os.walk — recursive directory tree","Beginner",
     "os.walk generates (root, dirs, files) tuples for every directory in a tree.",
     """import os, tempfile
base = os.path.join(tempfile.gettempdir(), "walk_demo")
os.makedirs(os.path.join(base,"sub1"), exist_ok=True)
os.makedirs(os.path.join(base,"sub2"), exist_ok=True)
for name in ["a.txt","b.py","sub1/c.txt","sub2/d.txt"]:
    p = os.path.join(base, name)
    with open(p,"w") as f: f.write(name)

print("Directory tree:")
for root, dirs, files in os.walk(base):
    level = root.replace(base,"").count(os.sep)
    indent = "  " * level
    print(f"{indent}{os.path.basename(root)}/")
    for file in files:
        print(f"{indent}  {file}")
"""),

    # ── INTERMEDIATE 31–70 ──
    (31,"JSON read and write","Intermediate",
     "json.dump/load serialise Python dicts to JSON files and back.",
     """import json, tempfile, os
path = os.path.join(tempfile.gettempdir(), "data.json")

data = {
    "name": "Alice", "age": 28,
    "skills": ["Python","SQL","Docker"],
    "active": True
}

with open(path,"w") as f:
    json.dump(data, f, indent=2)

with open(path) as f:
    loaded = json.load(f)

print(loaded)
print("Name:", loaded["name"])
print("Skills:", loaded["skills"])
"""),

    (32,"CSV read and write","Intermediate",
     "csv.writer/reader handle commas, quotes, and newlines correctly.",
     """import csv, tempfile, os
path = os.path.join(tempfile.gettempdir(), "students.csv")

rows = [
    ["Name","Grade","Score"],
    ["Alice","A",95],["Bob","B",82],["Carol","A",91]
]
with open(path,"w",newline="") as f:
    csv.writer(f).writerows(rows)

with open(path) as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(f"{row['Name']:8} | {row['Grade']} | {row['Score']}")
"""),

    (33,"Read large file with generator","Intermediate",
     "Yield lines from a generator to process huge files without loading them into memory.",
     """import tempfile, os
path = os.path.join(tempfile.gettempdir(), "big.txt")
with open(path,"w") as f:
    for i in range(1000): f.write(f"line {i}: data\\n")

def read_lines(filepath, skip_blank=True):
    with open(filepath) as f:
        for line in f:
            stripped = line.rstrip()
            if skip_blank and not stripped:
                continue
            yield stripped

count = sum(1 for _ in read_lines(path))
print(f"Processed {count} lines via generator")
"""),

    (34,"File search with glob","Intermediate",
     "glob.glob and Path.glob find files matching wildcard patterns.",
     """import glob, tempfile, os
from pathlib import Path

d = tempfile.gettempdir()
for ext in ["py","txt","json"]:
    open(os.path.join(d,f"glob_test.{ext}"),"w").close()

# glob.glob
py_files = glob.glob(os.path.join(d,"glob_test.*"))
print("glob.glob matches:")
for f in py_files: print(" ", os.path.basename(f))

# pathlib glob
print("\\nPath.glob matches:")
for p in Path(d).glob("glob_test.*"):
    print(" ", p.name)
"""),

    (35,"Temporary files with tempfile","Intermediate",
     "tempfile.NamedTemporaryFile creates a temp file deleted automatically on close.",
     """import tempfile

# NamedTemporaryFile
with tempfile.NamedTemporaryFile(mode="w", suffix=".txt",
                                  delete=False) as f:
    f.write("temporary content")
    name = f.name
    print("Temp file:", name)

with open(name) as f:
    print("Content:", f.read())

import os; os.remove(name)
print("Cleaned up:", not os.path.exists(name))

# SpooledTemporaryFile — stays in memory until threshold
with tempfile.SpooledTemporaryFile(max_size=1024, mode="w+") as f:
    f.write("in-memory"); f.seek(0)
    print("Spooled:", f.read())
"""),

    (36,"File locking pattern","Intermediate",
     "Use a lock file to prevent concurrent writes from multiple processes.",
     """import os, tempfile, time

lock_path = os.path.join(tempfile.gettempdir(), "app.lock")

def acquire_lock(lock):
    if os.path.exists(lock):
        return False
    with open(lock,"w") as f:
        f.write(str(os.getpid()))
    return True

def release_lock(lock):
    if os.path.exists(lock):
        os.remove(lock)

if acquire_lock(lock_path):
    print("Lock acquired, doing work...")
    time.sleep(0)   # simulate work
    release_lock(lock_path)
    print("Lock released")
else:
    print("Another process holds the lock")
"""),

    (37,"Read config from INI file","Intermediate",
     "configparser reads .ini / .cfg style configuration files into sections.",
     """import configparser, tempfile, os
path = os.path.join(tempfile.gettempdir(), "config.ini")

config_text = \"\"\"
[database]
host = localhost
port = 5432
name = mydb

[logging]
level = DEBUG
file = app.log
\"\"\"
with open(path,"w") as f: f.write(config_text)

cfg = configparser.ConfigParser()
cfg.read(path)

print("DB host :", cfg["database"]["host"])
print("DB port :", cfg.getint("database","port"))
print("Log level:", cfg["logging"]["level"])
print("Sections :", cfg.sections())
"""),

    (38,"Atomic file write (write-then-rename)","Intermediate",
     "Write to a temp file then rename — prevents corruption on crash mid-write.",
     """import os, tempfile

def atomic_write(path, content):
    dir_ = os.path.dirname(path) or "."
    fd, tmp = tempfile.mkstemp(dir=dir_)
    try:
        with os.fdopen(fd,"w") as f:
            f.write(content)
        os.replace(tmp, path)      # atomic on POSIX
        print(f"Atomically wrote to {path}")
    except Exception:
        os.remove(tmp)
        raise

target = os.path.join(tempfile.gettempdir(), "atomic.txt")
atomic_write(target, "safe content here")
with open(target) as f: print(f.read())
"""),

    (39,"Tail a file (last N lines)","Intermediate",
     "Efficient tail: seek near EOF and scan backwards without reading the whole file.",
     """import os, tempfile

def tail(filepath, n=5):
    with open(filepath,"rb") as f:
        f.seek(0, 2)
        size = f.tell()
        buf, lines_found = b"", 0
        ptr = size
        while ptr > 0 and lines_found < n:
            step = min(512, ptr)
            ptr -= step
            f.seek(ptr)
            buf = f.read(step) + buf
            lines_found = buf.count(b"\\n")
        return b"\\n".join(buf.split(b"\\n")[-n:]).decode()

path = os.path.join(tempfile.gettempdir(), "tail.txt")
with open(path,"w") as f:
    for i in range(20): f.write(f"log line {i}\\n")

print(tail(path, 5))
"""),

    (40,"Search text in file (grep-like)","Intermediate",
     "Yield matching lines with their line numbers — like a simple grep.",
     """import tempfile, os, re

def grep(pattern, filepath):
    regex = re.compile(pattern, re.IGNORECASE)
    with open(filepath) as f:
        for num, line in enumerate(f, 1):
            if regex.search(line):
                yield num, line.rstrip()

path = os.path.join(tempfile.gettempdir(), "grep.txt")
with open(path,"w") as f:
    f.write("Python is great\\nJava is verbose\\nPython rocks\\nC++ is fast\\n")

print("Lines matching 'python':")
for lineno, text in grep("python", path):
    print(f"  Line {lineno}: {text}")
"""),

    (41,"File checksum with hashlib","Intermediate",
     "Compute MD5/SHA256 of a file by reading it in chunks to handle large files.",
     """import hashlib, tempfile, os

def file_hash(path, algorithm="sha256"):
    h = hashlib.new(algorithm)
    with open(path,"rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

path = os.path.join(tempfile.gettempdir(), "hash.txt")
with open(path,"w") as f: f.write("hash me please")

print("MD5   :", file_hash(path,"md5"))
print("SHA256:", file_hash(path,"sha256"))
"""),

    (42,"Zip archive creation","Intermediate",
     "zipfile.ZipFile creates and reads .zip archives without external tools.",
     """import zipfile, tempfile, os
d = tempfile.gettempdir()
zip_path = os.path.join(d,"archive.zip")

files = {}
for name in ["a.txt","b.txt","c.txt"]:
    p = os.path.join(d,name)
    with open(p,"w") as f: f.write(f"Content of {name}")
    files[name] = p

with zipfile.ZipFile(zip_path,"w", zipfile.ZIP_DEFLATED) as zf:
    for name, path in files.items():
        zf.write(path, arcname=name)

print("Archive contents:")
with zipfile.ZipFile(zip_path,"r") as zf:
    for info in zf.infolist():
        print(f"  {info.filename:10} {info.file_size} bytes")
"""),

    (43,"Extract zip archive","Intermediate",
     "ZipFile.extractall() extracts all files; extract() extracts one at a time.",
     """import zipfile, tempfile, os
d = tempfile.gettempdir()
zip_path = os.path.join(d,"archive.zip")
extract_dir = os.path.join(d,"extracted")
os.makedirs(extract_dir, exist_ok=True)

# Use zip from example 42 if it exists, else create minimal one
if not os.path.exists(zip_path):
    with zipfile.ZipFile(zip_path,"w") as zf:
        zf.writestr("hello.txt","Hello from zip!")

with zipfile.ZipFile(zip_path,"r") as zf:
    zf.extractall(extract_dir)
    names = zf.namelist()

print("Extracted:", names)
for n in names:
    p = os.path.join(extract_dir, n)
    if os.path.isfile(p):
        with open(p) as f: print(f"  {n}: {f.read()[:40]}")
"""),

    (44,"Memory-mapped files with mmap","Intermediate",
     "mmap provides zero-copy access to file contents — reads/writes like a bytearray.",
     """import mmap, tempfile, os

path = os.path.join(tempfile.gettempdir(), "mmap.txt")
with open(path,"wb") as f:
    f.write(b"Hello, Memory Mapped World!")

with open(path,"r+b") as f:
    mm = mmap.mmap(f.fileno(), 0)
    print(mm[0:5])             # b'Hello'
    mm[7:13] = b"MEMORY"       # in-place edit
    mm.seek(0)
    print(mm.read())
    mm.close()
"""),

    (45,"Watch file for changes (polling)","Intermediate",
     "Poll os.path.getmtime() to detect when a file is modified.",
     """import os, time, tempfile

path = os.path.join(tempfile.gettempdir(), "watch.txt")
with open(path,"w") as f: f.write("initial")

def watch_once(filepath, interval=0.05, timeout=1):
    last_mtime = os.path.getmtime(filepath)
    deadline = time.time() + timeout
    while time.time() < deadline:
        mtime = os.path.getmtime(filepath)
        if mtime != last_mtime:
            return True, mtime
        time.sleep(interval)
    return False, last_mtime

# Modify the file
time.sleep(0.05)
with open(path,"a") as f: f.write("\\nmodified")

changed, mtime = watch_once(path)
print("File changed:", changed)
print("New mtime:", datetime.fromtimestamp(mtime))
"""),

    (46,"Read structured binary data with struct","Intermediate",
     "struct.pack/unpack converts between Python values and C-style binary data.",
     """import struct, tempfile, os

path = os.path.join(tempfile.gettempdir(), "binary.dat")

# Pack: 1 int (4 bytes) + 1 float (4 bytes) + 2 shorts (2+2)
fmt = "!ifHH"   # big-endian: int,float,ushort,ushort
data = (42, 3.14, 100, 200)
packed = struct.pack(fmt, *data)

with open(path,"wb") as f: f.write(packed)

with open(path,"rb") as f: raw = f.read()

unpacked = struct.unpack(fmt, raw)
print("Packed size:", struct.calcsize(fmt), "bytes")
print("Unpacked:", unpacked)
"""),

    (47,"CSV DictWriter and DictReader","Intermediate",
     "DictWriter uses column names as keys; DictReader returns rows as dicts.",
     """import csv, tempfile, os
path = os.path.join(tempfile.gettempdir(), "people.csv")

people = [
    {"name":"Alice","age":28,"city":"Delhi"},
    {"name":"Bob",  "age":32,"city":"Mumbai"},
    {"name":"Carol","age":25,"city":"Pune"},
]

with open(path,"w",newline="") as f:
    w = csv.DictWriter(f, fieldnames=["name","age","city"])
    w.writeheader()
    w.writerows(people)

print("CSV File:")
with open(path) as f: print(f.read())

print("\\nRead back:")
with open(path) as f:
    for row in csv.DictReader(f):
        print(dict(row))
"""),

    (48,"Recursive file search","Intermediate",
     "Path.rglob() or os.walk recursively find files matching a pattern.",
     """import tempfile, os
from pathlib import Path

base = Path(tempfile.gettempdir()) / "rglob_demo"
(base/"sub/deep").mkdir(parents=True, exist_ok=True)

files = ["a.txt","b.py","sub/c.txt","sub/d.py","sub/deep/e.txt"]
for f in files:
    (base/f).write_text(f"content of {f}")

print("All .txt files:")
for p in base.rglob("*.txt"):
    print(" ", p.relative_to(base))

print("\\nAll .py files:")
for p in base.rglob("*.py"):
    print(" ", p.relative_to(base))
"""),

    (49,"Directory tree size","Intermediate",
     "Walk the directory tree and sum all file sizes.",
     """import os, tempfile

def dir_size(path):
    total = 0
    for root, dirs, files in os.walk(path):
        for f in files:
            try: total += os.path.getsize(os.path.join(root,f))
            except OSError: pass
    return total

d = tempfile.gettempdir()
size = dir_size(d)
print(f"Temp dir size: {size:,} bytes ({size/1024/1024:.2f} MB)")
"""),

    (50,"File metadata with os.stat","Intermediate",
     "os.stat returns size, permissions, creation/modification timestamps.",
     """import os, stat, tempfile
from datetime import datetime

path = os.path.join(tempfile.gettempdir(), "meta.txt")
with open(path,"w") as f: f.write("metadata test")

s = os.stat(path)
print(f"Size    : {s.st_size} bytes")
print(f"Modified: {datetime.fromtimestamp(s.st_mtime)}")
print(f"Accessed: {datetime.fromtimestamp(s.st_atime)}")
mode = stat.filemode(s.st_mode)
print(f"Mode    : {mode}")
"""),

    (51,"Read/write JSONL (JSON Lines)","Intermediate",
     "JSONL stores one JSON object per line — efficient for streaming large datasets.",
     """import json, tempfile, os

path = os.path.join(tempfile.gettempdir(), "data.jsonl")

records = [
    {"id":1,"event":"login", "user":"alice"},
    {"id":2,"event":"upload","user":"bob"},
    {"id":3,"event":"logout","user":"alice"},
]

with open(path,"w") as f:
    for r in records: f.write(json.dumps(r)+"\n")

print("JSONL file:")
with open(path) as f: print(f.read())

print("Parsed records:")
with open(path) as f:
    for line in f:
        print(json.loads(line))
"""),

    (52,"Backup a file with timestamp","Intermediate",
     "Before overwriting, copy the original with a timestamp suffix.",
     """import shutil, os, tempfile
from datetime import datetime

def backup(filepath):
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    bak = f"{filepath}.bak_{ts}"
    shutil.copy2(filepath, bak)
    return bak

path = os.path.join(tempfile.gettempdir(), "important.txt")
with open(path,"w") as f: f.write("Version 1")

bak = backup(path)
print("Backup created:", os.path.basename(bak))

with open(path,"w") as f: f.write("Version 2")
print("Current:", open(path).read())
print("Backup :", open(bak).read())
"""),

    (53,"Find duplicate files by hash","Intermediate",
     "Group files by their SHA256 checksum to find exact duplicates.",
     """import hashlib, os, tempfile
from collections import defaultdict

def hash_file(path):
    h = hashlib.sha256()
    with open(path,"rb") as f:
        for chunk in iter(lambda: f.read(8192), b""): h.update(chunk)
    return h.hexdigest()

d = tempfile.gettempdir()
for name, content in [("dup1.txt","same"),("dup2.txt","same"),("uniq.txt","different")]:
    with open(os.path.join(d,name),"w") as f: f.write(content)

groups = defaultdict(list)
for name in ["dup1.txt","dup2.txt","uniq.txt"]:
    p = os.path.join(d,name)
    groups[hash_file(p)].append(name)

for h, files in groups.items():
    if len(files) > 1:
        print(f"Duplicates ({h[:8]}...): {files}")
    else:
        print(f"Unique: {files[0]}")
"""),

    (54,"Log rotation (manual)","Intermediate",
     "Rotate a log file when it exceeds a size limit, keeping N backups.",
     """import os, shutil, tempfile

def rotate_log(path, max_bytes=200, keep=3):
    if os.path.exists(path) and os.path.getsize(path) >= max_bytes:
        for i in range(keep-1, 0, -1):
            src = f"{path}.{i}"; dst = f"{path}.{i+1}"
            if os.path.exists(src): shutil.move(src, dst)
        shutil.move(path, f"{path}.1")
        print("Rotated log")

path = os.path.join(tempfile.gettempdir(), "rotate.log")
for i in range(10):
    with open(path,"a") as f: f.write(f"log entry {i}\\n")
    rotate_log(path, max_bytes=50)

for f in sorted(os.listdir(tempfile.gettempdir())):
    if "rotate.log" in f:
        print(f"{f}: {os.path.getsize(os.path.join(tempfile.gettempdir(),f))} bytes")
"""),

    (55,"Read file in reverse","Intermediate",
     "Efficiently read a text file from the last line to the first.",
     """import tempfile, os

def reverse_lines(filepath):
    with open(filepath,"rb") as f:
        f.seek(0,2); pos = f.tell()
        buf = b""
        while pos > 0:
            step = min(512, pos); pos -= step
            f.seek(pos); buf = f.read(step) + buf
            while b"\\n" in buf:
                buf, _, line = buf.rpartition(b"\\n")
                if line: yield line.decode()
        if buf: yield buf.decode()

path = os.path.join(tempfile.gettempdir(), "rev.txt")
with open(path,"w") as f:
    for i in range(1,6): f.write(f"Line {i}\\n")

print("Reversed:")
for line in reverse_lines(path):
    print(" ", line)
"""),

    (56,"Path operations with pathlib","Intermediate",
     "pathlib.Path provides an expressive, OOP interface for all path manipulations.",
     """from pathlib import Path
import tempfile

base = Path(tempfile.gettempdir()) / "pl_demo"
base.mkdir(exist_ok=True)

# Create nested structure
(base/"src"/"utils").mkdir(parents=True, exist_ok=True)
(base/"src"/"utils"/"helper.py").write_text("# helper")
(base/"src"/"main.py").write_text("# main")
(base/"README.md").write_text("# Project")

print("All files:")
for p in base.rglob("*"):
    if p.is_file():
        print(" ", p.relative_to(base))

readme = base/"README.md"
print("\\nREADME stem  :", readme.stem)
print("README suffix:", readme.suffix)
print("New name     :", readme.with_suffix(".txt").name)
"""),

    (57,"Context manager for safe writes","Intermediate",
     "Custom context manager rolls back a write if an exception occurs.",
     """import os, tempfile

class SafeWriter:
    def __init__(self, path):
        self.path = path
        d = os.path.dirname(path) or tempfile.gettempdir()
        self._fd, self._tmp = tempfile.mkstemp(dir=d)
        self._file = os.fdopen(self._fd, "w")
    def __enter__(self):
        return self._file
    def __exit__(self, exc_type, *_):
        self._file.close()
        if exc_type is None:
            os.replace(self._tmp, self.path); print("Write committed")
        else:
            os.remove(self._tmp); print("Write rolled back")

target = os.path.join(tempfile.gettempdir(), "safe.txt")
with SafeWriter(target) as f:
    f.write("safe data")

with open(target) as f: print(f.read())
"""),

    (58,"Compress file with gzip","Intermediate",
     "gzip module reads/writes .gz files; compresses on the fly.",
     """import gzip, tempfile, os

path = os.path.join(tempfile.gettempdir(), "data.txt.gz")
original = "Python " * 200   # repetitive text compresses well

with gzip.open(path,"wt", encoding="utf-8") as f:
    f.write(original)

with gzip.open(path,"rt", encoding="utf-8") as f:
    restored = f.read()

raw_size = len(original.encode())
gz_size  = os.path.getsize(path)
print(f"Original : {raw_size:,} bytes")
print(f"Gzipped  : {gz_size:,} bytes")
print(f"Ratio    : {gz_size/raw_size*100:.1f}%")
print(f"Match    : {original == restored}")
"""),

    (59,"Redirect stdout to a file","Intermediate",
     "Use contextlib.redirect_stdout to capture print() output to a file.",
     """import contextlib, tempfile, os

path = os.path.join(tempfile.gettempdir(), "captured.txt")

with open(path,"w") as f:
    with contextlib.redirect_stdout(f):
        print("This goes to the file")
        for i in range(1,6):
            print(f"  item {i}: {i**2}")

with open(path) as f:
    print("Captured output:")
    print(f.read())
"""),

    (60,"Multi-file batch processing","Intermediate",
     "Process all .txt files in a directory and write a summary report.",
     """import os, tempfile
from pathlib import Path

d = Path(tempfile.gettempdir()) / "batch"
d.mkdir(exist_ok=True)

words = ["apple banana cherry","foo bar","hello world python","one two three four"]
for i, w in enumerate(words):
    (d/f"file{i}.txt").write_text(w)

report = []
for txt in d.glob("*.txt"):
    content = txt.read_text()
    wc = len(content.split())
    report.append({"file":txt.name,"words":wc,"chars":len(content)})

print(f"{'File':<12} {'Words':>6} {'Chars':>6}")
print("-"*26)
for r in sorted(report, key=lambda x: x["file"]):
    print(f"{r['file']:<12} {r['words']:>6} {r['chars']:>6}")
print(f"{'TOTAL':<12} {sum(r['words'] for r in report):>6}")
"""),

    (61,"Sparse file with seek","Intermediate",
     "Create a large sparse file by seeking past data (OS stores only written blocks).",
     """import tempfile, os

path = os.path.join(tempfile.gettempdir(), "sparse.bin")
with open(path,"wb") as f:
    f.seek(1024*1024 - 1)   # seek to 1 MB - 1
    f.write(b"\\x00")        # write one byte at end

actual = os.path.getsize(path)
print(f"File size   : {actual:,} bytes (1 MB)")
"""),

    (62,"File watcher using mtime","Intermediate",
     "Poll modification time to detect changes in a watched file or directory.",
     """import os, time, tempfile, hashlib

def file_fingerprint(path):
    h = hashlib.md5()
    with open(path,"rb") as f:
        for chunk in iter(lambda: f.read(4096), b""): h.update(chunk)
    return h.hexdigest()

path = os.path.join(tempfile.gettempdir(), "watched.txt")
with open(path,"w") as f: f.write("initial content")

fp_before = file_fingerprint(path)
with open(path,"a") as f: f.write("\\nnew line added")
fp_after = file_fingerprint(path)

print("Before fingerprint:", fp_before[:16])
print("After  fingerprint:", fp_after[:16])
print("Changed:", fp_before != fp_after)
"""),

    (63,"Parse log file","Intermediate",
     "Extract structured data from a plain-text log file using regex.",
     """import re, tempfile, os

log_text = \"\"\"2024-01-15 10:23:45 INFO  Server started
2024-01-15 10:24:01 ERROR Database connection failed
2024-01-15 10:24:05 INFO  Retrying connection
2024-01-15 10:24:07 WARN  Slow query detected (2.3s)
2024-01-15 10:25:00 INFO  Connection restored
\"\"\"
path = os.path.join(tempfile.gettempdir(), "app.log")
with open(path,"w") as f: f.write(log_text)

pattern = re.compile(r"(\\d{4}-\\d{2}-\\d{2} \\d{2}:\\d{2}:\\d{2}) (\\w+) +(.+)")
errors = []
with open(path) as f:
    for line in f:
        m = pattern.match(line)
        if m:
            ts, level, msg = m.groups()
            if level in ("ERROR","WARN"):
                errors.append({"ts":ts,"level":level,"msg":msg})

print("Errors/Warnings:")
for e in errors:
    print(f"  [{e['level']}] {e['ts']} — {e['msg']}")
"""),

    (64,"CSV to JSON conversion","Intermediate",
     "Read a CSV file and write it as a JSON array of objects.",
     """import csv, json, tempfile, os

d = tempfile.gettempdir()
csv_path  = os.path.join(d,"students.csv")
json_path = os.path.join(d,"students.json")

with open(csv_path,"w",newline="") as f:
    w = csv.DictWriter(f,fieldnames=["name","grade","score"])
    w.writeheader()
    w.writerows([{"name":"Alice","grade":"A","score":"95"},
                 {"name":"Bob",  "grade":"B","score":"82"}])

with open(csv_path) as f:
    data = list(csv.DictReader(f))

with open(json_path,"w") as f:
    json.dump(data, f, indent=2)

print("JSON output:")
print(open(json_path).read())
"""),

    (65,"Walk and find large files","Intermediate",
     "Recursively search a directory tree for files above a size threshold.",
     """import os, tempfile

def find_large(root, min_bytes=500):
    results = []
    for dirpath, _, files in os.walk(root):
        for fname in files:
            p = os.path.join(dirpath, fname)
            try:
                s = os.path.getsize(p)
                if s >= min_bytes: results.append((s, p))
            except OSError: pass
    return sorted(results, reverse=True)

d = tempfile.gettempdir()
# Ensure a large-ish file exists
p = os.path.join(d,"large.txt")
with open(p,"w") as f: f.write("X"*2000)

large = find_large(d, min_bytes=1000)[:5]
print("Top 5 large files in temp:")
for size, path in large:
    print(f"  {size:>8,} bytes  {os.path.basename(path)}")
"""),

    (66,"Pickle — serialise Python objects","Intermediate",
     "pickle serialises any Python object to bytes; use for caching or inter-process data.",
     """import pickle, tempfile, os

class Config:
    def __init__(self, **kw):
        self.__dict__.update(kw)

cfg = Config(debug=True, db="postgres://localhost/app", workers=4)

path = os.path.join(tempfile.gettempdir(), "config.pkl")
with open(path,"wb") as f:
    pickle.dump(cfg, f, protocol=pickle.HIGHEST_PROTOCOL)

with open(path,"rb") as f:
    loaded = pickle.load(f)

print("Loaded config:")
print("  debug  :", loaded.debug)
print("  db     :", loaded.db)
print("  workers:", loaded.workers)
"""),

    (67,"Line-by-line file transformation","Intermediate",
     "Read input line by line, transform, and write to output without buffering all in memory.",
     """import tempfile, os

src = os.path.join(tempfile.gettempdir(), "transform_in.txt")
dst = os.path.join(tempfile.gettempdir(), "transform_out.txt")

with open(src,"w") as f:
    f.write("  hello world  \\n  python rocks  \\n  file handling  \\n")

with open(src) as fin, open(dst,"w") as fout:
    for line in fin:
        transformed = line.strip().upper().replace(" ","_")
        fout.write(transformed + "\\n")

print("Output:")
print(open(dst).read())
"""),

    (68,"File permissions","Intermediate",
     "os.chmod changes file permissions using octal or stat constants.",
     """import os, stat, tempfile

path = os.path.join(tempfile.gettempdir(), "perms.txt")
with open(path,"w") as f: f.write("permission demo")

# Read-only
os.chmod(path, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)
s = os.stat(path)
print("Read-only mode :", stat.filemode(s.st_mode))

# Restore read-write
os.chmod(path, stat.S_IRUSR | stat.S_IWUSR)
s = os.stat(path)
print("Read-write mode:", stat.filemode(s.st_mode))
"""),

    (69,"Merge multiple files","Intermediate",
     "Concatenate several files into one output file efficiently.",
     """import tempfile, os

d = tempfile.gettempdir()
parts = []
for i in range(1,4):
    p = os.path.join(d,f"part{i}.txt")
    with open(p,"w") as f: f.write(f"--- Part {i} ---\\nContent {i}\\n")
    parts.append(p)

merged = os.path.join(d,"merged.txt")
with open(merged,"w") as out:
    for path in parts:
        with open(path) as f:
            out.write(f.read())

print("Merged file:")
print(open(merged).read())
"""),

    (70,"Watch directory for new files","Intermediate",
     "Compare directory snapshots to detect added/removed files.",
     """import os, time, tempfile

def snapshot(directory):
    return {f: os.path.getmtime(os.path.join(directory,f))
            for f in os.listdir(directory)
            if os.path.isfile(os.path.join(directory,f))}

d = tempfile.gettempdir()
before = snapshot(d)

# Simulate new file
new_file = os.path.join(d,"watcher_new.txt")
with open(new_file,"w") as f: f.write("new!")

after = snapshot(d)
added   = set(after) - set(before)
removed = set(before) - set(after)

print("Added  :", added)
print("Removed:", removed)
"""),

    # ── ADVANCED 71–100 ──
    (71,"Custom file-like object","Advanced",
     "Implement __enter__, __exit__, read(), write() to create a custom IO object.",
     """class InMemoryFile:
    def __init__(self, initial=""):
        self._buf = list(initial)
        self._pos = 0
    def write(self, s):
        self._buf[self._pos:self._pos+len(s)] = list(s)
        self._pos += len(s)
    def read(self, n=-1):
        if n == -1: n = len(self._buf) - self._pos
        data = "".join(self._buf[self._pos:self._pos+n])
        self._pos += n; return data
    def seek(self, pos): self._pos = pos
    def tell(self): return self._pos
    def getvalue(self): return "".join(self._buf)
    def __enter__(self): return self
    def __exit__(self, *_): pass

with InMemoryFile() as f:
    f.write("Hello "); f.write("World")
    f.seek(6)
    print(f.read())       # World
    print(f.getvalue())   # Hello World
"""),

    (72,"Lazy file reader (generator pipeline)","Advanced",
     "Chain generator functions to process files lazily in a Unix-pipeline style.",
     """import tempfile, os

def open_file(path):
    with open(path) as f:
        yield from f

def strip_lines(lines):
    for line in lines: yield line.strip()

def filter_comments(lines):
    for line in lines:
        if line and not line.startswith("#"): yield line

def to_upper(lines):
    for line in lines: yield line.upper()

path = os.path.join(tempfile.gettempdir(), "pipe.txt")
with open(path,"w") as f:
    f.write("# comment\\nhello world\\n# skip\\npython rocks\\n")

pipeline = to_upper(filter_comments(strip_lines(open_file(path))))
for line in pipeline:
    print(line)
"""),

    (73,"Virtual filesystem (dict-based)","Advanced",
     "Simulate a filesystem entirely in memory using a nested dict.",
     """class VFS:
    def __init__(self): self._fs = {}
    def write(self, path, content):
        self._fs[path] = content
    def read(self, path):
        if path not in self._fs: raise FileNotFoundError(path)
        return self._fs[path]
    def delete(self, path): del self._fs[path]
    def ls(self, prefix="/"):
        return [p for p in self._fs if p.startswith(prefix)]
    def exists(self, path): return path in self._fs

vfs = VFS()
vfs.write("/etc/config.ini","[db]\\nhost=localhost")
vfs.write("/var/log/app.log","2024-01-01 INFO started")
vfs.write("/home/user/notes.txt","meeting at 3pm")

print("Files:", vfs.ls())
print("Config:", vfs.read("/etc/config.ini"))
vfs.delete("/var/log/app.log")
print("After delete:", vfs.ls())
"""),

    (74,"File diff (line-by-line)","Advanced",
     "Use difflib.unified_diff to compare two files like the Unix diff command.",
     """import difflib, tempfile, os

d = tempfile.gettempdir()
f1 = os.path.join(d,"v1.txt"); f2 = os.path.join(d,"v2.txt")

with open(f1,"w") as f:
    f.write("line 1\\nline 2\\nline 3\\nline 4\\n")
with open(f2,"w") as f:
    f.write("line 1\\nLINE 2 CHANGED\\nline 3\\nnew line 4.5\\nline 4\\n")

with open(f1) as a, open(f2) as b:
    diff = list(difflib.unified_diff(
        a.readlines(), b.readlines(),
        fromfile="v1.txt", tofile="v2.txt"
    ))

print("".join(diff))
"""),

    (75,"Trie-indexed file search","Advanced",
     "Index words from files in a Trie for O(m) prefix lookups.",
     """import tempfile, os

class Trie:
    def __init__(self): self.root={}
    def insert(self,w,src):
        n=self.root
        for c in w: n=n.setdefault(c,{})
        n.setdefault("$",[]).append(src)
    def search(self,prefix):
        n=self.root
        for c in prefix:
            if c not in n: return []
            n=n[c]
        results=[]
        def dfs(node):
            if "$" in node: results.extend(node["$"])
            for k,v in node.items():
                if k!="$": dfs(v)
        dfs(n); return list(set(results))

trie = Trie()
d = tempfile.gettempdir()
corpus = {"doc1.txt":"python file handling rocks","doc2.txt":"python lists are flexible"}
for fname,text in corpus.items():
    p = os.path.join(d,fname)
    with open(p,"w") as f: f.write(text)
    for word in text.split(): trie.insert(word, fname)

print("Files with 'py...':  ", trie.search("py"))
print("Files with 'file...':", trie.search("file"))
"""),

    (76,"Multi-part file splitter","Advanced",
     "Split a large file into N equal chunks; reassemble them correctly.",
     """import os, tempfile, math

def split_file(path, n_parts):
    size = os.path.getsize(path)
    chunk = math.ceil(size / n_parts)
    parts = []
    with open(path,"rb") as f:
        for i in range(n_parts):
            data = f.read(chunk)
            if not data: break
            p = f"{path}.part{i}"
            with open(p,"wb") as out: out.write(data)
            parts.append(p)
    return parts

def join_files(parts, out_path):
    with open(out_path,"wb") as out:
        for p in parts:
            with open(p,"rb") as f: out.write(f.read())

d = tempfile.gettempdir()
src = os.path.join(d,"split_src.txt")
with open(src,"w") as f: f.write("ABCDEFGHIJKLMNOPQRSTUVWXYZ"*4)

parts = split_file(src, 4)
print("Parts:", [os.path.basename(p) for p in parts])
print("Sizes:", [os.path.getsize(p) for p in parts])

out = os.path.join(d,"reassembled.txt")
join_files(parts, out)
original = open(src).read(); restored = open(out).read()
print("Reassembly match:", original == restored)
"""),

    (77,"Event-sourced file log","Advanced",
     "Append JSON events to a log file; replay them to reconstruct state.",
     """import json, os, tempfile

class EventLog:
    def __init__(self, path):
        self.path = path
    def append(self, event):
        with open(self.path,"a") as f:
            f.write(json.dumps(event)+"\n")
    def replay(self):
        state = {"balance":0,"txns":[]}
        if not os.path.exists(self.path): return state
        with open(self.path) as f:
            for line in f:
                e = json.loads(line)
                if e["type"]=="credit":  state["balance"]+=e["amount"]
                elif e["type"]=="debit": state["balance"]-=e["amount"]
                state["txns"].append(e)
        return state

log = EventLog(os.path.join(tempfile.gettempdir(),"events.jsonl"))
log.append({"type":"credit","amount":1000,"note":"salary"})
log.append({"type":"debit", "amount":300, "note":"rent"})
log.append({"type":"credit","amount":500, "note":"bonus"})
state = log.replay()
print(f"Balance : ₹{state['balance']}")
print(f"Transactions: {len(state['txns'])}")
"""),

    (78,"Async file I/O simulation","Advanced",
     "Simulate async file reads using threading + queue for concurrent I/O.",
     """import threading, queue, tempfile, os, time

def async_read(path, result_queue):
    try:
        with open(path) as f:
            data = f.read()
            result_queue.put(("ok", path, data))
    except Exception as e:
        result_queue.put(("err", path, str(e)))

d = tempfile.gettempdir()
paths = []
for i in range(4):
    p = os.path.join(d,f"async_{i}.txt")
    with open(p,"w") as f: f.write(f"File {i} content")
    paths.append(p)

q = queue.Queue()
threads = [threading.Thread(target=async_read,args=(p,q)) for p in paths]
for t in threads: t.start()
for t in threads: t.join()

results = []
while not q.empty(): results.append(q.get())
for status, path, data in results:
    print(f"[{status.upper()}] {os.path.basename(path)}: {data}")
"""),

    (79,"B-tree file index (simulation)","Advanced",
     "Build a simple keyword→line_number index for instant search in large files.",
     """import tempfile, os, json
from collections import defaultdict

def build_index(filepath):
    index = defaultdict(list)
    with open(filepath) as f:
        for lineno, line in enumerate(f,1):
            for word in set(line.lower().split()):
                word = word.strip(".,!?")
                if word: index[word].append(lineno)
    return dict(index)

d = tempfile.gettempdir()
text_path = os.path.join(d,"indexed.txt")
idx_path  = os.path.join(d,"index.json")

with open(text_path,"w") as f:
    f.write("Python is awesome\\nFile handling in Python is powerful\\nPython rocks\\n")

index = build_index(text_path)
with open(idx_path,"w") as f: json.dump(index,f,indent=2)

print("Index built. Searching 'python':", index.get("python",[]))
print("Searching 'handling':", index.get("handling",[]))
print("Index size:", len(index), "unique words")
"""),

    (80,"Rolling hash file deduplication","Advanced",
     "Use Rabin-Karp rolling hash to detect duplicate content blocks in files.",
     """import tempfile, os

BASE, MOD = 31, 10**9+9

def rolling_hash(data, window=8):
    hashes = set()
    n = len(data)
    if n < window: return {hash(data)}
    h = 0
    for c in data[:window]: h = (h*BASE + ord(c)) % MOD
    hashes.add(h)
    bp = pow(BASE, window-1, MOD)
    for i in range(window, n):
        h = (h - ord(data[i-window])*bp) % MOD
        h = (h*BASE + ord(data[i])) % MOD
        hashes.add(h)
    return hashes

d = tempfile.gettempdir()
for name, content in [("rh1.txt","Hello World Hello"),("rh2.txt","Hello World Goodbye")]:
    with open(os.path.join(d,name),"w") as f: f.write(content)

c1 = open(os.path.join(d,"rh1.txt")).read()
c2 = open(os.path.join(d,"rh2.txt")).read()
h1, h2 = rolling_hash(c1), rolling_hash(c2)
common = h1 & h2
print(f"File 1 blocks: {len(h1)}")
print(f"File 2 blocks: {len(h2)}")
print(f"Common blocks: {len(common)}")
print(f"Similarity  : {len(common)/max(len(h1),len(h2))*100:.0f}%")
"""),

    (81,"File tagging system","Advanced",
     "Store file tags in a JSON sidecar file for custom metadata.",
     """import json, os, tempfile
from pathlib import Path

class FileTagger:
    def __init__(self, store_path):
        self.store = Path(store_path)
        self._data = json.loads(self.store.read_text()) if self.store.exists() else {}
    def tag(self, filepath, *tags):
        k = str(Path(filepath).resolve())
        self._data.setdefault(k,[])
        self._data[k] = list(set(self._data[k]+list(tags)))
        self.store.write_text(json.dumps(self._data,indent=2))
    def get_tags(self, filepath):
        return self._data.get(str(Path(filepath).resolve()),[])
    def find_by_tag(self, tag):
        return [f for f,tags in self._data.items() if tag in tags]

d = tempfile.gettempdir()
tagger = FileTagger(os.path.join(d,"tags.json"))
files = ["report.txt","data.csv","script.py"]
for fname in files:
    p = os.path.join(d,fname)
    with open(p,"w") as f: f.write(fname)

tagger.tag(os.path.join(d,"report.txt"),"important","finance")
tagger.tag(os.path.join(d,"data.csv"), "data","finance")
tagger.tag(os.path.join(d,"script.py"),"code","automation")

print("Tags on report.txt :", tagger.get_tags(os.path.join(d,"report.txt")))
print("Files tagged 'finance':", [os.path.basename(f) for f in tagger.find_by_tag("finance")])
"""),

    (82,"Write-ahead log (WAL) pattern","Advanced",
     "Log every change before applying it — the basis of database crash recovery.",
     """import json, os, tempfile

class WAL:
    def __init__(self, wal_path, data_path):
        self.wal  = wal_path
        self.data = data_path
        self.state = self._load_data()
    def _load_data(self):
        if os.path.exists(self.data):
            return json.loads(open(self.data).read())
        return {}
    def apply(self, key, value):
        # 1. Write to WAL first
        with open(self.wal,"a") as f:
            f.write(json.dumps({"key":key,"value":value})+"\n")
        # 2. Apply to state
        self.state[key] = value
        # 3. Checkpoint to data file
        with open(self.data,"w") as f:
            json.dump(self.state, f)
    def recover(self):
        if not os.path.exists(self.wal): return 0
        count = 0
        with open(self.wal) as f:
            for line in f:
                e = json.loads(line); self.state[e["key"]]=e["value"]; count+=1
        return count

d = tempfile.gettempdir()
wal = WAL(os.path.join(d,"app.wal"),os.path.join(d,"app.db"))
wal.apply("user:1","Alice"); wal.apply("user:2","Bob"); wal.apply("setting:theme","dark")
print("State:", wal.state)
n = wal.recover()
print(f"Recovered {n} entries from WAL")
"""),

    (83,"Encrypted file storage","Advanced",
     "XOR-cipher demo for encrypted file storage (use cryptography lib for production).",
     """import os, tempfile

def xor_encrypt(data: bytes, key: bytes) -> bytes:
    return bytes(b ^ key[i % len(key)] for i, b in enumerate(data))

def write_encrypted(path, text, key):
    encrypted = xor_encrypt(text.encode(), key.encode())
    with open(path,"wb") as f: f.write(encrypted)

def read_decrypted(path, key):
    with open(path,"rb") as f: raw = f.read()
    return xor_encrypt(raw, key.encode()).decode()

path = os.path.join(tempfile.gettempdir(), "secret.enc")
key  = "MySecretKey123"
msg  = "Top secret message: Python is great!"

write_encrypted(path, msg, key)
raw   = open(path,"rb").read()
plain = read_decrypted(path, key)

print("Encrypted (hex):", raw[:20].hex(), "...")
print("Decrypted      :", plain)
print("Match          :", plain == msg)
"""),

    (84,"File content versioning","Advanced",
     "Keep a numbered history of file versions with diff summaries.",
     """import os, shutil, difflib, tempfile

class VersionedFile:
    def __init__(self, path):
        self.path = path
        self.hist = os.path.join(tempfile.gettempdir(), "versions")
        os.makedirs(self.hist, exist_ok=True)
        self.v = 0
    def save(self, content):
        self.v += 1
        ver_path = os.path.join(self.hist, f"v{self.v}.txt")
        with open(ver_path,"w") as f: f.write(content)
        with open(self.path,"w") as f: f.write(content)
        print(f"Saved version {self.v}")
    def diff(self, v1, v2):
        f1 = open(os.path.join(self.hist,f"v{v1}.txt")).readlines()
        f2 = open(os.path.join(self.hist,f"v{v2}.txt")).readlines()
        return "".join(difflib.unified_diff(f1,f2,fromfile=f"v{v1}",tofile=f"v{v2}"))

vf = VersionedFile(os.path.join(tempfile.gettempdir(),"versioned.txt"))
vf.save("line 1\\nline 2\\nline 3\\n")
vf.save("line 1\\nLINE 2 MODIFIED\\nline 3\\nline 4 added\\n")

print("\\nDiff v1 → v2:")
print(vf.diff(1,2))
"""),

    (85,"Concurrent file writer (thread-safe)","Advanced",
     "Use threading.Lock to prevent race conditions when multiple threads write to a file.",
     """import threading, tempfile, os

class ThreadSafeLogger:
    def __init__(self, path):
        self.path = path
        self.lock = threading.Lock()
    def log(self, msg):
        with self.lock:
            with open(self.path,"a") as f:
                f.write(f"[{threading.current_thread().name}] {msg}\\n")

logger = ThreadSafeLogger(os.path.join(tempfile.gettempdir(),"threaded.log"))

def worker(tid):
    for i in range(3):
        logger.log(f"Task {tid}-{i}")

threads = [threading.Thread(target=worker, args=(i,), name=f"T{i}") for i in range(4)]
for t in threads: t.start()
for t in threads: t.join()

with open(logger.path) as f: lines = f.readlines()
print(f"Total log entries: {len(lines)}")
for l in lines[:6]: print(" ", l.rstrip())
"""),

    (86,"File stream transformer","Advanced",
     "Wrap any file object in a transformer that modifies content on the fly.",
     """import io, tempfile, os

class UpperCaseStream(io.TextIOWrapper):
    def write(self, s):
        return super().write(s.upper())

path = os.path.join(tempfile.gettempdir(), "stream.txt")
raw = open(path,"wb")
with UpperCaseStream(io.BufferedWriter(raw), encoding="utf-8") as f:
    f.write("hello world\\n")
    f.write("python file handling\\n")

print("Written with UpperCaseStream:")
print(open(path).read())
"""),

    (87,"Chunked file upload simulation","Advanced",
     "Simulate multi-chunk file upload: split, transmit (copy), reassemble.",
     """import os, tempfile, hashlib

def upload_chunked(src, dest_dir, chunk_size=512):
    os.makedirs(dest_dir, exist_ok=True)
    chunks = []
    with open(src,"rb") as f:
        idx = 0
        while True:
            data = f.read(chunk_size)
            if not data: break
            p = os.path.join(dest_dir,f"chunk_{idx:04d}.bin")
            with open(p,"wb") as c: c.write(data)
            chunks.append(p); idx+=1
    return chunks

def assemble(chunks, dest):
    with open(dest,"wb") as out:
        for c in sorted(chunks):
            with open(c,"rb") as f: out.write(f.read())

def sha(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for c in iter(lambda:f.read(4096),b""): h.update(c)
    return h.hexdigest()

d = tempfile.gettempdir()
src = os.path.join(d,"upload_src.txt")
with open(src,"w") as f: f.write("Data to upload "*100)

chunks = upload_chunked(src, os.path.join(d,"chunks"))
print(f"Uploaded in {len(chunks)} chunks")

dst = os.path.join(d,"assembled.txt")
assemble(chunks, dst)
print("Integrity check:", sha(src) == sha(dst))
"""),

    (88,"Hot-reloadable config file","Advanced",
     "Re-read a config JSON file whenever its modification time changes.",
     """import json, os, time, tempfile

class HotConfig:
    def __init__(self, path):
        self.path = path
        self._mtime = None
        self._cfg   = {}
        self._reload()
    def _reload(self):
        m = os.path.getmtime(self.path)
        if m != self._mtime:
            with open(self.path) as f:
                self._cfg = json.load(f)
            self._mtime = m
            print("Config reloaded")
    def get(self, key, default=None):
        self._reload()
        return self._cfg.get(key, default)

path = os.path.join(tempfile.gettempdir(), "hotcfg.json")
with open(path,"w") as f: json.dump({"debug":False,"workers":2}, f)

cfg = HotConfig(path)
print("debug:", cfg.get("debug"))

# Simulate config change
time.sleep(0.05)
import os; os.utime(path, None)   # touch
with open(path,"w") as f: json.dump({"debug":True,"workers":8}, f)

print("debug after change:", cfg.get("debug"))
print("workers:", cfg.get("workers"))
"""),

    (89,"Merkle tree file integrity","Advanced",
     "Build a Merkle tree over file chunks for tamper detection.",
     """import hashlib, tempfile, os

def sha256(data): return hashlib.sha256(data).hexdigest()

def merkle_root(chunks):
    layer = [sha256(c) for c in chunks]
    while len(layer) > 1:
        if len(layer)%2: layer.append(layer[-1])
        layer = [sha256((layer[i]+layer[i+1]).encode())
                 for i in range(0, len(layer), 2)]
    return layer[0]

path = os.path.join(tempfile.gettempdir(), "merkle.txt")
with open(path,"wb") as f: f.write(os.urandom(1024))

with open(path,"rb") as f:
    chunks = []
    while True:
        c=f.read(64)
        if not c: break
        chunks.append(c)

root = merkle_root(chunks)
print(f"Chunks  : {len(chunks)}")
print(f"Root    : {root[:32]}...")

# Tamper one chunk
chunks[5] = b"tampered"*8
tampered_root = merkle_root(chunks)
print(f"Tampered: {tampered_root[:32]}...")
print(f"Integrity OK: {root == tampered_root}")
"""),

    (90,"Streaming CSV processor","Advanced",
     "Process a huge CSV row-by-row without loading it into memory.",
     """import csv, tempfile, os, statistics

def stream_csv(path):
    with open(path,newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield row

path = os.path.join(tempfile.gettempdir(), "stream.csv")
import random
with open(path,"w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=["id","score","grade"])
    w.writeheader()
    for i in range(1000):
        s=random.randint(40,100)
        w.writerow({"id":i,"score":s,"grade":"A" if s>=90 else "B" if s>=75 else "C"})

scores=[]; grades={"A":0,"B":0,"C":0}
for row in stream_csv(path):
    scores.append(int(row["score"]))
    grades[row["grade"]]+=1

print(f"Records  : {len(scores)}")
print(f"Mean     : {statistics.mean(scores):.1f}")
print(f"Std dev  : {statistics.stdev(scores):.1f}")
print(f"Grades   : {grades}")
"""),

    (91,"File-based pub/sub system","Advanced",
     "Processes communicate via watched files (filesystem-based message bus).",
     """import json, os, time, tempfile, threading

class FileBus:
    def __init__(self, base):
        self.base = base
        os.makedirs(base, exist_ok=True)
    def publish(self, topic, msg):
        ts = time.time()
        p  = os.path.join(self.base, f"{topic}_{ts}.msg")
        with open(p,"w") as f: json.dump({"ts":ts,"msg":msg}, f)
    def consume(self, topic):
        msgs = []
        for fname in sorted(os.listdir(self.base)):
            if fname.startswith(topic):
                p = os.path.join(self.base, fname)
                with open(p) as f: msgs.append(json.load(f))
                os.remove(p)
        return msgs

bus = FileBus(os.path.join(tempfile.gettempdir(),"filebus"))
bus.publish("orders","Order #1: 2x Python Book")
bus.publish("orders","Order #2: 1x Keyboard")
bus.publish("alerts","Disk space low!")

print("Orders:", [m["msg"] for m in bus.consume("orders")])
print("Alerts:", [m["msg"] for m in bus.consume("alerts")])
"""),

    (92,"Copy-on-write file proxy","Advanced",
     "Read from original; only write to a copy when the first mutation occurs.",
     """import shutil, os, tempfile

class CopyOnWrite:
    def __init__(self, src):
        self.src  = src
        self._copy = None
    def _ensure_copy(self):
        if not self._copy:
            self._copy = self.src + ".cow"
            shutil.copy2(self.src, self._copy)
            print("COW: copy created")
    def read(self):
        path = self._copy or self.src
        with open(path) as f: return f.read()
    def write(self, content):
        self._ensure_copy()
        with open(self._copy,"w") as f: f.write(content)
    def commit(self):
        if self._copy:
            os.replace(self._copy, self.src)
            self._copy = None; print("COW: committed")

d = tempfile.gettempdir()
orig = os.path.join(d,"cow_orig.txt")
with open(orig,"w") as f: f.write("Original content")

cow = CopyOnWrite(orig)
print("Read (no copy yet):", cow.read())
cow.write("Modified content")
print("Read (from copy)  :", cow.read())
cow.commit()
print("After commit      :", open(orig).read())
"""),

    (93,"Directory mirroring (rsync-like)","Advanced",
     "Sync two directories: copy new/changed files, optionally delete removed ones.",
     """import os, shutil, hashlib, tempfile

def file_hash(path):
    h=hashlib.md5()
    with open(path,"rb") as f:
        for c in iter(lambda:f.read(4096),b""): h.update(c)
    return h.hexdigest()

def mirror(src, dst):
    os.makedirs(dst, exist_ok=True)
    copied=deleted=skipped=0
    for fname in os.listdir(src):
        s=os.path.join(src,fname); d=os.path.join(dst,fname)
        if not os.path.exists(d) or file_hash(s)!=file_hash(d):
            shutil.copy2(s,d); copied+=1
        else: skipped+=1
    print(f"Mirrored: +{copied} copied, ={skipped} skipped")

d = tempfile.gettempdir()
src_dir=os.path.join(d,"mirror_src"); dst_dir=os.path.join(d,"mirror_dst")
os.makedirs(src_dir,exist_ok=True)
for i in range(4):
    with open(os.path.join(src_dir,f"f{i}.txt"),"w") as f: f.write(f"file {i}"*10)

mirror(src_dir, dst_dir)
with open(os.path.join(src_dir,"f0.txt"),"w") as f: f.write("updated content"*10)
mirror(src_dir, dst_dir)   # only f0 should be re-copied
"""),

    (94,"Append-only ledger file","Advanced",
     "Immutable append-only log with hash chaining for tamper evidence.",
     """import json, hashlib, os, tempfile

class Ledger:
    def __init__(self, path):
        self.path = path
        self.prev_hash = "0"*64
        if os.path.exists(path):
            with open(path) as f:
                for line in f: pass   # fast-forward to last hash
            self.prev_hash = json.loads(line)["hash"]
    def append(self, data):
        entry = {"data":data,"prev":self.prev_hash}
        entry_hash = hashlib.sha256(json.dumps(entry,sort_keys=True).encode()).hexdigest()
        entry["hash"] = entry_hash
        with open(self.path,"a") as f: f.write(json.dumps(entry)+"\n")
        self.prev_hash = entry_hash
        return entry_hash
    def verify(self):
        prev = "0"*64
        with open(self.path) as f:
            for line in f:
                e=json.loads(line)
                if e["prev"]!=prev: return False
                h=hashlib.sha256(json.dumps({"data":e["data"],"prev":e["prev"]},sort_keys=True).encode()).hexdigest()
                if h!=e["hash"]: return False
                prev=e["hash"]
        return True

led = Ledger(os.path.join(tempfile.gettempdir(),"ledger.jsonl"))
led.append({"amount":500,"type":"credit"})
led.append({"amount":200,"type":"debit"})
led.append({"amount":100,"type":"debit"})
print("Ledger valid:", led.verify())
"""),

    (95,"Binary file format parser","Advanced",
     "Define a simple binary file format and implement read/write.",
     """import struct, os, tempfile

# Format: magic(4) + version(2) + record_count(4) + records[id(4)+value(4)]
MAGIC = b"PYDB"

def write_db(path, records):
    with open(path,"wb") as f:
        f.write(struct.pack("!4sHI", MAGIC, 1, len(records)))
        for rid, val in records:
            f.write(struct.pack("!ii", rid, val))

def read_db(path):
    with open(path,"rb") as f:
        magic, ver, count = struct.unpack("!4sHI", f.read(10))
        assert magic==MAGIC, "Bad magic"
        records=[]
        for _ in range(count):
            records.append(struct.unpack("!ii", f.read(8)))
    return ver, records

path = os.path.join(tempfile.gettempdir(), "data.pydb")
write_db(path, [(1,100),(2,200),(3,300),(4,400)])
ver, records = read_db(path)
print(f"Version: {ver}, Records: {len(records)}")
for r in records: print(f"  id={r[0]}, value={r[1]}")
"""),

    (96,"File-based cache with TTL","Advanced",
     "Cache expensive results to disk; invalidate entries older than TTL seconds.",
     """import json, os, time, hashlib, tempfile

class FileCache:
    def __init__(self, cache_dir, ttl=60):
        self.dir = cache_dir; self.ttl = ttl
        os.makedirs(cache_dir, exist_ok=True)
    def _key(self, k): return os.path.join(self.dir, hashlib.md5(k.encode()).hexdigest()+".json")
    def get(self, key):
        p = self._key(key)
        if not os.path.exists(p): return None
        with open(p) as f: entry=json.load(f)
        if time.time()-entry["ts"] > self.ttl:
            os.remove(p); return None
        return entry["value"]
    def set(self, key, value):
        with open(self._key(key),"w") as f:
            json.dump({"ts":time.time(),"value":value}, f)

cache = FileCache(os.path.join(tempfile.gettempdir(),"cache"), ttl=10)
cache.set("pi", 3.14159265)
cache.set("greeting","hello world")

print("pi       :", cache.get("pi"))
print("greeting :", cache.get("greeting"))
print("missing  :", cache.get("nonexistent"))
"""),

    (97,"Nested archive extractor","Advanced",
     "Recursively extract .zip files, including zips inside zips.",
     """import zipfile, os, tempfile, io

def extract_recursive(zip_path, dest):
    os.makedirs(dest, exist_ok=True)
    with zipfile.ZipFile(zip_path) as zf:
        for name in zf.namelist():
            if name.endswith(".zip"):
                data = zf.read(name)
                sub_dest = os.path.join(dest, name[:-4])
                extract_recursive(io.BytesIO(data), sub_dest)
            else:
                zf.extract(name, dest)

d = tempfile.gettempdir()
# Create inner zip
inner_zip = os.path.join(d,"inner.zip")
with zipfile.ZipFile(inner_zip,"w") as zf:
    zf.writestr("deep.txt","I was inside a zip inside a zip!")

# Create outer zip containing inner
outer_zip = os.path.join(d,"outer.zip")
with zipfile.ZipFile(outer_zip,"w") as zf:
    zf.writestr("top.txt","Top level file")
    zf.write(inner_zip,"inner.zip")

extract_recursive(outer_zip, os.path.join(d,"extracted_nested"))
for root,dirs,files in os.walk(os.path.join(d,"extracted_nested")):
    for f in files:
        p=os.path.join(root,f)
        print(f.ljust(12), "→", open(p).read() if p.endswith(".txt") else "(binary)")
"""),

    (98,"Real-time file tail with callback","Advanced",
     "Continuously tail a growing file and call a callback for each new line.",
     """import os, time, tempfile, threading

class FileTailer:
    def __init__(self, path, callback, poll=0.05):
        self.path=path; self.callback=callback; self.poll=poll
        self._stop=threading.Event()
    def start(self):
        self._t=threading.Thread(target=self._run, daemon=True)
        self._t.start()
    def stop(self): self._stop.set(); self._t.join()
    def _run(self):
        with open(self.path) as f:
            f.seek(0,2)   # start at end
            while not self._stop.is_set():
                line=f.readline()
                if line: self.callback(line.rstrip())
                else: time.sleep(self.poll)

path = os.path.join(tempfile.gettempdir(), "tail_live.log")
with open(path,"w") as f: pass   # create empty

received = []
tailer = FileTailer(path, lambda l: received.append(l))
tailer.start()

with open(path,"a") as f:
    for i in range(5): f.write(f"log {i}\\n"); f.flush(); time.sleep(0.06)

time.sleep(0.2); tailer.stop()
print(f"Tailed {len(received)} lines:")
for l in received: print(" ", l)
"""),

    (99,"File deduplication engine","Advanced",
     "Scan a directory, find duplicates by hash, and produce a dedup report.",
     """import os, hashlib, tempfile
from collections import defaultdict
from pathlib import Path

def scan(directory):
    groups = defaultdict(list)
    for root,_,files in os.walk(directory):
        for f in files:
            p=os.path.join(root,f)
            h=hashlib.md5(open(p,"rb").read()).hexdigest()
            groups[h].append(p)
    return {h:ps for h,ps in groups.items() if len(ps)>1}

d = tempfile.gettempdir()
base = os.path.join(d,"dedup_test")
os.makedirs(base, exist_ok=True)
for name,content in [("a.txt","same content"),("b.txt","same content"),
                      ("c.txt","different"),("d.txt","same content"),("e.txt","unique")]:
    with open(os.path.join(base,name),"w") as f: f.write(content)

dups = scan(base)
total_wasted = 0
print("Duplicate groups:")
for h, paths in dups.items():
    size = os.path.getsize(paths[0])
    wasted = size*(len(paths)-1)
    total_wasted += wasted
    print(f"  Hash {h[:8]}... × {len(paths)} files ({size}B each)")
    for p in paths: print(f"    {os.path.basename(p)}")
print(f"Wasted space: {total_wasted} bytes")
"""),

    (100,"Full mini file system","Advanced",
     "In-memory filesystem with directories, files, permissions, and metadata — all in Python.",
     """import time, io

class FSNode:
    def __init__(self, name, is_dir=False, mode=0o644):
        self.name=name; self.is_dir=is_dir; self.mode=mode
        self.created=self.modified=time.time()
        self.children={}; self.data=b""
    @property
    def size(self): return len(self.data) if not self.is_dir else sum(c.size for c in self.children.values())

class MiniFS:
    def __init__(self):
        self.root=FSNode("/",is_dir=True,mode=0o755)
    def _resolve(self,path):
        parts=[p for p in path.strip("/").split("/") if p]
        node=self.root
        for part in parts:
            if part not in node.children: raise FileNotFoundError(path)
            node=node.children[part]
        return node
    def mkdir(self,path):
        parts=path.strip("/").split("/"); parent=self.root
        for part in parts[:-1]: parent=parent.children[part]
        parent.children[parts[-1]]=FSNode(parts[-1],is_dir=True)
    def write(self,path,data):
        parts=path.strip("/").split("/"); parent=self.root
        for part in parts[:-1]: parent=parent.children[part]
        node=parent.children.setdefault(parts[-1],FSNode(parts[-1]))
        node.data=data.encode() if isinstance(data,str) else data
        node.modified=time.time()
    def read(self,path):
        return self._resolve(path).data.decode()
    def ls(self,path="/"):
        node=self._resolve(path) if path!="/" else self.root
        return list(node.children.keys())
    def stat(self,path):
        n=self._resolve(path) if path!="/" else self.root
        return {"name":n.name,"size":n.size,"is_dir":n.is_dir,"mode":oct(n.mode)}

fs=MiniFS()
fs.mkdir("etc"); fs.mkdir("var"); fs.mkdir("home")
fs.write("etc/config.ini","[server]\\nport=8080")
fs.write("home/notes.txt","Meeting at 3pm")
fs.write("var/app.log","2024-01-01 INFO started")

print("Root  :", fs.ls("/"))
print("etc/  :", fs.ls("etc"))
print("Config:", fs.read("etc/config.ini"))
print("Stat  :", fs.stat("home/notes.txt"))
print("Root size:", fs.stat("/")["size"], "bytes")
"""),
]

# ──────────────────────────────────────────────────────────────────────
# SIDEBAR
# ──────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📂 File Handling")
    section = st.radio("Navigate to", [
        "🏠 Overview",
        "📄 File Object Methods",
        "🔓 open() Modes",
        "🗂️ os / shutil / pathlib",
        "🟢 Beginner (1–30)",
        "🔵 Intermediate (31–70)",
        "🟣 Advanced (71–100)",
        "🎮 Interactive Playground",
    ])
    st.markdown("---")
    st.markdown("**Quick Stats**")
    st.markdown("• 15 file object methods")
    st.markdown("• 12 open() modes")
    st.markdown("• 27 os/pathlib functions")
    st.markdown("• 100 code examples")

# ──────────────────────────────────────────────────────────────────────
# HERO
# ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class='hero'>
  <h1>📂 Python FILE HANDLING — Complete Reference</h1>
  <p>All Methods · All Modes · os · shutil · pathlib · 100 Examples · Beginner → Advanced</p>
</div>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────
# OVERVIEW
# ──────────────────────────────────────────────────────────────────────
def run_safe(code_src):
    buf = io.StringIO()
    env = {
        "__builtins__": __builtins__,
        "os":os,"io":io,"sys":sys,"shutil":shutil,"json":json,
        "csv":csv,"tempfile":tempfile,"pathlib":pathlib,"Path":Path,
        "stat":stat,"re":re,"datetime":datetime,"random":random,
        "time":time,"threading":__import__("threading"),
        "hashlib":__import__("hashlib"),"struct":__import__("struct"),
        "zipfile":__import__("zipfile"),"gzip":__import__("gzip"),
        "mmap":__import__("mmap"),"pickle":__import__("pickle"),
        "difflib":__import__("difflib"),"configparser":__import__("configparser"),
        "queue":__import__("queue"),"contextlib":contextlib,
        "statistics":__import__("statistics"),
        "SANDBOX": SANDBOX,
    }
    try:
        with contextlib.redirect_stdout(buf):
            exec(textwrap.dedent(code_src), env)
        return buf.getvalue() or "(no output)"
    except Exception:
        return traceback.format_exc()


if section == "🏠 Overview":
    st.markdown("""
<div class='stat-row'>
  <div class='stat-box'><div class='stat-num'>15</div><div class='stat-lbl'>File Methods</div></div>
  <div class='stat-box'><div class='stat-num'>12</div><div class='stat-lbl'>open() Modes</div></div>
  <div class='stat-box'><div class='stat-num'>27</div><div class='stat-lbl'>os/pathlib Functions</div></div>
  <div class='stat-box'><div class='stat-num'>100</div><div class='stat-lbl'>Code Examples</div></div>
</div>
""", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### 📖 What is File Handling?")
        st.markdown("""
File handling is the process of creating, reading, writing, and managing files on disk.

| Feature | Python Tool |
|---|---|
| Open / read / write | `open()` built-in |
| File object methods | `read`, `write`, `seek`… |
| Path operations | `os.path`, `pathlib.Path` |
| Copy / move / delete | `shutil` |
| JSON / CSV / Config | `json`, `csv`, `configparser` |
| Archives | `zipfile`, `gzip`, `tarfile` |
| Binary data | `struct`, `mmap` |

```python
with open("file.txt", "r") as f:
    content = f.read()
```
""")
    with c2:
        st.markdown("### 🗂️ What's Inside This App?")
        st.markdown("""
| Section | Contents |
|---|---|
| 📄 File Object Methods | 15 methods: read, write, seek, tell, flush… |
| 🔓 open() Modes | All 12 modes: r, w, a, x, b, + |
| 🗂️ os/shutil/pathlib | 27 functions for paths, dirs, copying |
| 🟢 Beginner | Create/read/write/delete, basic ops (1–30) |
| 🔵 Intermediate | JSON/CSV/zip/mmap/grep/watcher (31–70) |
| 🟣 Advanced | Custom FS, WAL, Merkle, threading (71–100) |
| 🎮 Playground | Live file operations in sandbox |
""")

    st.markdown("### ⚡ Quick Cheatsheet")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.code("""# Open modes
open(f, 'r')   # read
open(f, 'w')   # write
open(f, 'a')   # append
open(f, 'rb')  # binary""", language="python")
    with c2:
        st.code("""# Core operations
f.read()       # all content
f.readline()   # one line
f.readlines()  # list
f.write(s)     # write""", language="python")
    with c3:
        st.code("""# pathlib
from pathlib import Path
p = Path("file.txt")
p.read_text()
p.write_text(s)
p.exists()""", language="python")

# ──────────────────────────────────────────────────────────────────────
# FILE OBJECT METHODS
# ──────────────────────────────────────────────────────────────────────
elif section == "📄 File Object Methods":
    st.markdown("<div class='sec-header'>📄 All 15 File Object Methods</div>", unsafe_allow_html=True)
    for m in FILE_METHODS:
        with st.expander(f"🔹 `{m['name']}`", expanded=False):
            c1, c2 = st.columns([1,1])
            with c1:
                st.markdown(f"**Definition:** {m['definition']}")
                st.markdown(f"**Syntax:** `{m['syntax']}`")
                st.info(f"💡 {m['tip']}")
            with c2:
                st.code(m["example"], language="python")

# ──────────────────────────────────────────────────────────────────────
# OPEN MODES
# ──────────────────────────────────────────────────────────────────────
elif section == "🔓 open() Modes":
    st.markdown("<div class='sec-header'>🔓 All 12 open() Modes</div>", unsafe_allow_html=True)
    st.markdown("**Syntax:** `open(file, mode='r', encoding=None, errors=None, buffering=-1)`")
    for mode, desc in OPEN_MODES:
        st.markdown(f"""
<div class='card'>
  <div class='card-title'><code>'{mode}'</code></div>
  <div class='card-def'>{desc}</div>
</div>
""", unsafe_allow_html=True)

    st.markdown("### Mode Combinations Visualised")
    st.markdown("""
| Mode | Read | Write | Create | Truncate | Append | Binary |
|------|:----:|:-----:|:------:|:--------:|:------:|:------:|
| `r`  | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| `w`  | ❌ | ✅ | ✅ | ✅ | ❌ | ❌ |
| `a`  | ❌ | ✅ | ✅ | ❌ | ✅ | ❌ |
| `x`  | ❌ | ✅ | ✅* | ❌ | ❌ | ❌ |
| `r+` | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| `w+` | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| `a+` | ✅ | ✅ | ✅ | ❌ | ✅ | ❌ |
| `rb` | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ |
| `wb` | ❌ | ✅ | ✅ | ✅ | ❌ | ✅ |

*`x` raises FileExistsError if file already exists.
""")

# ──────────────────────────────────────────────────────────────────────
# OS / SHUTIL / PATHLIB
# ──────────────────────────────────────────────────────────────────────
elif section == "🗂️ os / shutil / pathlib":
    st.markdown("<div class='sec-header'>🗂️ os, shutil & pathlib Reference</div>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["🔧 os / shutil (27 functions)", "🗂️ pathlib.Path (28 methods)", "🔍 Quick Compare"])

    with tab1:
        for fn, desc in OS_FUNCTIONS:
            st.markdown(f"""
<div class='card'>
  <div class='card-title'><code>{fn}</code></div>
  <div class='card-def'>{desc}</div>
</div>
""", unsafe_allow_html=True)

    with tab2:
        for fn, desc in PATHLIB_METHODS:
            st.markdown(f"""
<div class='card'>
  <div class='card-title'><code>{fn}</code></div>
  <div class='card-def'>{desc}</div>
</div>
""", unsafe_allow_html=True)

    with tab3:
        st.markdown("""
| Task | `os` / `shutil` | `pathlib` |
|---|---|---|
| Read file | `open(p).read()` | `Path(p).read_text()` |
| Write file | `open(p,'w').write(s)` | `Path(p).write_text(s)` |
| File exists | `os.path.exists(p)` | `Path(p).exists()` |
| Join paths | `os.path.join(a,b)` | `Path(a) / b` |
| File name | `os.path.basename(p)` | `Path(p).name` |
| Extension | `os.path.splitext(p)[1]` | `Path(p).suffix` |
| Make dirs | `os.makedirs(p)` | `Path(p).mkdir(parents=True)` |
| List dir | `os.listdir(p)` | `Path(p).iterdir()` |
| Delete file | `os.remove(p)` | `Path(p).unlink()` |
| Glob | `glob.glob(pattern)` | `Path(p).glob(pattern)` |
| Move | `shutil.move(s,d)` | `Path(s).rename(d)` |
""")

# ──────────────────────────────────────────────────────────────────────
# EXAMPLE SECTIONS
# ──────────────────────────────────────────────────────────────────────
elif section in ("🟢 Beginner (1–30)", "🔵 Intermediate (31–70)", "🟣 Advanced (71–100)"):
    level_map = {
        "🟢 Beginner (1–30)":      ("Beginner",     "🟢", "badge-beg"),
        "🔵 Intermediate (31–70)": ("Intermediate", "🔵", "badge-int"),
        "🟣 Advanced (71–100)":    ("Advanced",     "🟣", "badge-adv"),
    }
    level_name, emoji, badge_cls = level_map[section]
    filtered = [(n,t,l,d,c) for n,t,l,d,c in EXAMPLES if l == level_name]

    st.markdown(
        f"<div class='sec-header'>{emoji} {level_name} — {len(filtered)} Examples</div>",
        unsafe_allow_html=True,
    )
    search = st.text_input("🔍 Search by title or keyword", "")

    for num, title, level, defn, code_src in filtered:
        if search and search.lower() not in title.lower() and search.lower() not in code_src.lower():
            continue
        with st.expander(f"#{num} — {title}", expanded=False):
            st.markdown(f"<span class='{badge_cls}'>{level}</span>", unsafe_allow_html=True)
            st.markdown(f"**📖 Definition:** {defn}")
            st.code(code_src, language="python")
            if st.button(f"▶ Run Example #{num}", key=f"run_{num}"):
                out = run_safe(code_src)
                st.markdown(f"<div class='out-box'>{out}</div>", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────
# INTERACTIVE PLAYGROUND
# ──────────────────────────────────────────────────────────────────────
elif section == "🎮 Interactive Playground":
    st.markdown("<div class='sec-header'>🎮 Interactive File Handling Playground</div>", unsafe_allow_html=True)
    st.info(f"📁 All files are created in a safe sandbox: `{SANDBOX}`")

    tab1, tab2, tab3 = st.tabs(["📝 Write & Read", "🗂️ Directory Ops", "✏️ Free Editor"])

    with tab1:
        st.markdown("### Write a file, then read it back")
        filename = st.text_input("Filename", "test.txt")
        content  = st.text_area("Content to write", "Hello, File Handling!\nLine 2\nLine 3")
        mode     = st.selectbox("Write mode", ["w (overwrite)", "a (append)"])
        if st.button("✍️ Write File"):
            p = SANDBOX / filename
            m = "w" if mode.startswith("w") else "a"
            p.write_text(content)
            st.markdown(f"<div class='out-box'>Written {len(content)} characters to {filename}</div>", unsafe_allow_html=True)

        if st.button("📖 Read File"):
            p = SANDBOX / filename
            if p.exists():
                txt = p.read_text()
                st.markdown(f"<div class='out-box'>{txt}</div>", unsafe_allow_html=True)
            else:
                st.warning("File not found — write it first!")

    with tab2:
        st.markdown("### Explore the Sandbox Directory")
        if st.button("🔄 Refresh listing"):
            pass
        files = list(SANDBOX.iterdir())
        if files:
            st.markdown("**Files in sandbox:**")
            for f in sorted(files):
                size = f.stat().st_size
                st.markdown(f"- `{f.name}` — {size} bytes")
        else:
            st.info("Sandbox is empty. Write a file first.")

        st.markdown("---")
        del_name = st.text_input("Delete a file by name", "")
        if st.button("🗑️ Delete File") and del_name:
            p = SANDBOX / del_name
            if p.exists():
                p.unlink()
                st.success(f"Deleted {del_name}")
            else:
                st.warning("File not found")

    with tab3:
        st.markdown("### ✏️ Free Code Editor")
        default_code = f"""# File Handling Playground
# All files are created in: {SANDBOX}
import os
from pathlib import Path

SANDBOX = Path(r"{SANDBOX}")

# Write a file
p = SANDBOX / "example.txt"
p.write_text("Python\\nFile\\nHandling\\n")

# Read it back
lines = p.read_text().splitlines()
for i, line in enumerate(lines, 1):
    print(f"Line {{i}}: {{line}}")

# File info
print(f"\\nFile: {{p.name}}")
print(f"Size: {{p.stat().st_size}} bytes")
print(f"Exists: {{p.exists()}}")
"""
        user_code = st.text_area("Python code:", default_code, height=260)
        if st.button("▶ Run Code", type="primary"):
            out = run_safe(user_code)
            st.markdown(f"<div class='out-box'>{out}</div>", unsafe_allow_html=True)

# FOOTER
st.markdown("---")
st.markdown(
    "<p style='text-align:center;color:#666;font-size:.85rem;'>"
    "📂 Python File Handling Complete Reference · 15 Methods · 12 Modes · 27 Functions · 100 Examples"
    "</p>",
    unsafe_allow_html=True,
)