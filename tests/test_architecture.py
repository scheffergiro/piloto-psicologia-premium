import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

class GenerationArchitectureTest(unittest.TestCase):
    def test_compatibility_entry_point_delegates_to_the_official_generator(self):
        wrapper=(ROOT/'gerar_retrato.py').read_text()
        self.assertIn('from gerar import gerar',wrapper)
        self.assertNotIn('read_text(',wrapper)
    def test_motion_asset_and_fonts_are_local(self):
        css=(ROOT/'src/styles.css').read_text()
        self.assertNotIn('fonts.googleapis',css)
        for name in ('PlayfairDisplay','DMSans'):
            self.assertTrue((ROOT/'src/assets/fonts'/f'{name}.ttf').is_file())
            self.assertIn('SIL OPEN FONT LICENSE',(ROOT/'src/assets/fonts'/f'{name}-OFL.txt').read_text())
        self.assertIn('prefers-reduced-motion',(ROOT/'src/motion.js').read_text())
