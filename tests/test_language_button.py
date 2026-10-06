from pathlib import Path
import subprocess
import unittest


ROOT = Path(__file__).resolve().parents[1]


class LanguageButtonTests(unittest.TestCase):
    def test_floating_language_button_runtime(self):
        result = subprocess.run(
            ['node', '--test', 'tests/test_language_button.mjs'],
            cwd=ROOT, capture_output=True, text=True, timeout=30,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
