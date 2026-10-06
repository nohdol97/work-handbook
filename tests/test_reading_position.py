from pathlib import Path
import subprocess
import unittest


ROOT = Path(__file__).resolve().parents[1]


class ReadingPositionTests(unittest.TestCase):
    def test_language_navigation_runtime(self):
        result = subprocess.run(
            ['node', '--test', 'tests/test_reading_position.mjs'],
            cwd=ROOT, capture_output=True, text=True, timeout=30,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
