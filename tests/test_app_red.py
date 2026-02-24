import unittest
from pathlib import Path


class DateCalculatorAppRedTests(unittest.TestCase):
    def setUp(self):
        self.repo_root = Path(__file__).resolve().parents[1]
        self.html_path = self.repo_root / "src" / "static" / "index.html"
        self.css_path = self.repo_root / "src" / "static" / "style.css"
        self.js_path = self.repo_root / "src" / "static" / "script.js"
        self.dockerfile_path = self.repo_root / "Dockerfile"

    def test_html_exists_and_has_datetime_inputs(self):
        self.assertTrue(self.html_path.exists(), "index.html が存在しません")
        html = self.html_path.read_text(encoding="utf-8")
        self.assertIn('type="datetime-local"', html)
        self.assertIn('id="start-datetime"', html)
        self.assertIn('id="end-datetime"', html)
        self.assertIn('id="base-datetime"', html)

    def test_html_has_day_offset_inputs_and_actions(self):
        self.assertTrue(self.html_path.exists(), "index.html が存在しません")
        html = self.html_path.read_text(encoding="utf-8")
        self.assertIn('id="day-offset"', html)
        self.assertIn('id="calculate-diff"', html)
        self.assertIn('id="calculate-offset"', html)

    def test_html_has_dark_mode_toggle(self):
        self.assertTrue(self.html_path.exists(), "index.html が存在しません")
        html = self.html_path.read_text(encoding="utf-8")
        self.assertIn('id="dark-mode-toggle"', html)

    def test_html_has_analog_clock_anchor_at_page_top(self):
        self.assertTrue(self.html_path.exists(), "index.html が存在しません")
        html = self.html_path.read_text(encoding="utf-8")
        self.assertIn('id="analog-clock"', html)

    def test_script_exists_and_implements_required_handlers(self):
        self.assertTrue(self.js_path.exists(), "script.js が存在しません")
        script = self.js_path.read_text(encoding="utf-8")
        self.assertIn('calculateDateDifference', script)
        self.assertIn('calculateOffsetDate', script)
        self.assertIn('dark-mode', script)

    def test_style_exists_and_defines_dark_mode_styles(self):
        self.assertTrue(self.css_path.exists(), "style.css が存在しません")
        css = self.css_path.read_text(encoding="utf-8")
        self.assertIn('.dark-mode', css)

    def test_style_has_stylish_animations(self):
        self.assertTrue(self.css_path.exists(), "style.css が存在しません")
        css = self.css_path.read_text(encoding="utf-8")
        self.assertIn('@keyframes', css)
        self.assertIn('animation:', css)

    def test_dockerfile_exists_and_uses_python_http_server(self):
        self.assertTrue(self.dockerfile_path.exists(), "Dockerfile が存在しません")
        dockerfile = self.dockerfile_path.read_text(encoding="utf-8")
        self.assertIn('python:3.11-slim', dockerfile)
        self.assertIn('http.server', dockerfile)


if __name__ == "__main__":
    unittest.main()
