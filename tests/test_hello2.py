# tests/test_type_error.py
import subprocess, sys
from pathlib import Path
import pytest

@pytest.mark.parametrize("file,errmsg", [
    ("type_error.ei", "Operazione '+' non supportata tra int e string"),
])
def test_type_error(tmp_path):
    project = Path(__file__).parent.parent
    cli = project / "cli" / "main.py"
    example = project / "examples" / "type_error.ei"
    res = subprocess.run(
        [sys.executable, str(cli), "run", str(example)],
        capture_output=True, text=True
    )
    assert res.returncode != 0
    assert errmsg in res.stderr or errmsg in res.stdout
