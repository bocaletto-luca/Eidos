# tests/test_hello.py
import subprocess
import sys
from pathlib import Path

def test_hello_world(tmp_path):
    # percorsi relativi al project root
    project = Path(__file__).parent.parent
    cli_script = project / "cli" / "main.py"
    example   = project / "examples" / "hello.ei"

    # esegui il comando
    res = subprocess.run(
        [sys.executable, str(cli_script), str(example)],
        capture_output=True, text=True
    )
    assert res.returncode == 0
    # stripping per evitare CR/LF
    assert res.stdout.strip() == "Hello, World!"
