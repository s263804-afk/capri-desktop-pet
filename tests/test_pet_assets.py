import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts' / 'pet_assets.py'


class PetAssetsTests(unittest.TestCase):
    def command(self, *args):
        return subprocess.run([sys.executable, str(SCRIPT), *map(str, args)], capture_output=True, text=True, encoding='utf-8')

    def test_extract_and_assemble_actual_asset_preserves_all_rgba_pixels(self):
        if not SCRIPT.is_file():
            self.fail('portable atlas utility has not been implemented')
        atlas = ROOT / 'assets' / 'spritesheet.png'
        with tempfile.TemporaryDirectory() as temp:
            temp = Path(temp)
            extracted = self.command('extract', atlas, '--out', temp / 'frames')
            self.assertEqual(extracted.returncode, 0, extracted.stderr)
            files = list((temp / 'frames').rglob('*.png'))
            self.assertEqual(len(files), 73)
            with Image.open(atlas) as original:
                with Image.open(temp / 'frames' / 'look' / '270.png') as left:
                    self.assertEqual(left.tobytes(), original.convert('RGBA').crop((768,2080,960,2288)).tobytes())
            rebuilt = self.command('assemble', temp / 'frames', '--out', temp / 'rebuilt.png')
            self.assertEqual(rebuilt.returncode, 0, rebuilt.stderr)
            with Image.open(atlas) as a, Image.open(temp / 'rebuilt.png') as b:
                self.assertEqual(a.convert('RGBA').tobytes(), b.convert('RGBA').tobytes())

    def test_missing_frame_is_rejected_without_creating_output(self):
        if not SCRIPT.is_file():
            self.fail('portable atlas utility has not been implemented')
        with tempfile.TemporaryDirectory() as temp:
            temp = Path(temp)
            (temp / 'frames').mkdir()
            result = self.command('assemble', temp / 'frames', '--out', temp / 'rebuilt.png')
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('missing frame', result.stderr.lower())
            self.assertFalse((temp / 'rebuilt.png').exists())

    def test_invalid_atlases_are_rejected(self):
        if not SCRIPT.is_file():
            self.fail('portable atlas utility has not been implemented')
        atlas = ROOT / 'assets' / 'spritesheet.png'
        for issue in ('empty-used-cell', 'unused-cell', 'opaque-background', 'wrong-size'):
            with self.subTest(issue=issue), tempfile.TemporaryDirectory() as temp:
                with Image.open(atlas) as source:
                    image = source.convert('RGBA')
                if issue == 'empty-used-cell':
                    image.paste((0,0,0,0), (0,0,192,208))
                elif issue == 'unused-cell':
                    image.putpixel((6*192+40,40), (255,0,0,255))
                elif issue == 'opaque-background':
                    image.putalpha(255)
                else:
                    image = image.crop((0,0,100,100))
                path = Path(temp) / 'invalid.png'
                image.save(path)
                result = self.command('validate', path)
                self.assertNotEqual(result.returncode, 0)
                self.assertFalse(json.loads(result.stdout)['ok'])


if __name__ == '__main__':
    unittest.main()
