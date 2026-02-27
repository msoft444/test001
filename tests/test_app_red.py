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
        self.assertIn('class="clock"', html)

    def test_html_is_self_contained_without_external_css_js_dependencies(self):
        self.assertTrue(self.html_path.exists(), "index.html が存在しません")
        html = self.html_path.read_text(encoding="utf-8")
        self.assertIn("<style>", html)
        self.assertIn("<script>", html)
        self.assertNotIn('rel="stylesheet"', html)
        self.assertNotIn('src="script.js"', html)

    def test_html_has_world_map_and_local_time(self):
        self.assertTrue(self.html_path.exists(), "index.html が存在しません")
        html = self.html_path.read_text(encoding="utf-8")
        self.assertIn('id="world-map"', html)
        self.assertIn('class="world-clock-container"', html)
        self.assertIn('id="selected-city-name"', html)
        self.assertIn('id="selected-city-time"', html)
        self.assertIn('updateWorldClock', html)
        self.assertIn('Tokyo', html)  # Default city

    def test_world_map_svg_is_detailed_enough_to_be_recognizable(self):
        self.assertTrue(self.html_path.exists(), "index.html が存在しません")
        html = self.html_path.read_text(encoding="utf-8")
        self.assertIn('class="world-map-svg"', html)
        self.assertIn('viewBox="0 0 200 100"', html)
        self.assertGreaterEqual(
            html.count('<path d="'),
            18,
            "世界地図の輪郭パス数が不足しており、地図としての判別性が低い可能性があります",
        )
        self.assertIn("Antarctica", html)

    def test_world_map_has_visual_aids_for_readability_in_both_modes(self):
        self.assertTrue(self.html_path.exists(), "index.html が存在しません")
        html = self.html_path.read_text(encoding="utf-8")
        self.assertIn(".map-container::before", html)
        self.assertIn("repeating-linear-gradient", html)
        self.assertIn("body.dark-mode .map-container::before", html)
        self.assertIn(".world-map-svg path", html)
        self.assertIn("body.dark-mode .world-map-svg path", html)

    def test_world_clock_is_rendered_right_of_analog_clock_in_header(self):
        self.assertTrue(self.html_path.exists(), "index.html が存在しません")
        html = self.html_path.read_text(encoding="utf-8")
        clock_index = html.find('<div class="clock" id="analog-clock">')
        world_clock_index = html.find('<div class="world-clock-container">')
        self.assertNotEqual(clock_index, -1)
        self.assertNotEqual(world_clock_index, -1)
        self.assertGreater(world_clock_index, clock_index)
        self.assertIn('<div class="clock-container">', html)

    def test_inline_style_contains_stylish_ui_and_clock_layout_rules(self):
        self.assertTrue(self.html_path.exists(), "index.html が存在しません")
        html = self.html_path.read_text(encoding="utf-8")
        self.assertIn(".clock {", html)
        self.assertIn(".number1", html)
        self.assertIn(".card {", html)
        self.assertIn(".toggle-switch", html)
        self.assertIn("@keyframes fadeInUp", html)

    def test_inline_script_contains_clock_update_loop(self):
        self.assertTrue(self.html_path.exists(), "index.html が存在しません")
        html = self.html_path.read_text(encoding="utf-8")
        self.assertIn("function updateClock()", html)
        self.assertIn("document.querySelector('.hand.second')", html)
        self.assertIn("setInterval(updateClock, 1000)", html)

    def test_inline_script_supports_city_selection_and_local_time_updates(self):
        self.assertTrue(self.html_path.exists(), "index.html が存在しません")
        html = self.html_path.read_text(encoding="utf-8")
        self.assertIn("const cities = [", html)
        self.assertIn("tz:", html)
        self.assertIn("function initMap()", html)
        self.assertIn("function selectCity(city)", html)
        self.assertIn("document.addEventListener(\"DOMContentLoaded\", initMap)", html)
        self.assertIn("new Intl.DateTimeFormat('ja-JP', options)", html)
        self.assertIn("setInterval(updateWorldClock, 1000)", html)

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
