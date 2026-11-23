"""Make sure a champion model exists before the API tests import app.py."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

if not (ROOT / "models" / "champion.joblib").exists():
    subprocess.run([sys.executable, str(ROOT / "train.py")], check=True, cwd=ROOT)
