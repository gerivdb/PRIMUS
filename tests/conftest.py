import sys
from pathlib import Path

# Allow `src.primus.*` imports when running pytest from repo root or tests/
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
