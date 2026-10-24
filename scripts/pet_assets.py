#!/usr/bin/env python3
"""Inspect, extract, and assemble the project's transparent v2 sprite atlas.

This is a structural asset utility, not the ChatGPT/Pets import validator.
It never redraws, rescales, mirrors, or removes disconnected flame components.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((ROOT / 'assets' / 'manifest.json').read_text(encoding='utf-8'))
CELL = (SCHEMA['cell_width'], SCHEMA['cell_height'])
SIZE = (SCHEMA['width'], SCHEMA['height'])
MAX_BYTES = 20 * 1024 * 1024


def frame_slots():
    for row in SCHEMA['rows']:
        for column, name in enumerate(row['frame_names']):
            yield row['row'], column, name


def cell_box(row: int, column: int):
    x, y = column * CELL[0], row * CELL[1]
    return x, y, x + CELL[0], y + CELL[1]


def inspect_image(image: Image.Image) -> list[str]:
    errors = []
    if image.size != SIZE:
        return [f'expected {SIZE[0]}x{SIZE[1]}, got {image.width}x{image.height}']
    alpha = image.convert('RGBA').getchannel('A')
    required = {(row, col) for row, col, _ in frame_slots()}
    for row in range(len(SCHEMA['rows'])):
        for column in range(SCHEMA['columns']):
            histogram = alpha.crop(cell_box(row, column)).histogram()
            visible = sum(histogram[1:])
            if (row, column) in required:
                if visible < 50:
                    errors.append(f'row {row} column {column}: missing artwork')
                elif visible > CELL[0] * CELL[1] * 0.95:
                    errors.append(f'row {row} column {column}: background is almost opaque')
            elif visible:
                errors.append(f'row {row} column {column}: unused cell is not transparent')
    return errors


def validate(path: Path) -> dict:
    raw = path.read_bytes()
    with Image.open(path) as image:
        errors = inspect_image(image)
        if image.format not in ('PNG', 'WEBP'):
            errors.append('expected a PNG or WebP file')
        dimensions = list(image.size)
    if len(raw) > MAX_BYTES:
        errors.append('file exceeds 20 MiB')
    return {'ok': not errors, 'file': path.name, 'sprite_version': 2,
            'dimensions': dimensions, 'required_frames': SCHEMA['required_frames'],
            'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest(), 'errors': errors}


def extract(source: Path, destination: Path) -> dict:
    report = validate(source)
    if not report['ok']:
        raise ValueError('; '.join(report['errors']))
    if destination.exists() and (not destination.is_dir() or any(destination.iterdir())):
        raise ValueError('output directory must be absent or empty; existing files will not be overwritten')
    with Image.open(source) as opened:
        image = opened.convert('RGBA')
        for row, column, name in frame_slots():
            output = destination / name
            output.parent.mkdir(parents=True, exist_ok=True)
            image.crop(cell_box(row, column)).save(output, format='PNG')
    return {'ok': True, 'extracted_frames': SCHEMA['required_frames']}


def assemble(source: Path, destination: Path) -> dict:
    if destination.exists():
        raise ValueError('output file already exists; choose a new filename')
    if destination.suffix.lower() != '.png':
        raise ValueError('assembled output must use a .png extension')
    image = Image.new('RGBA', SIZE, (0, 0, 0, 0))
    for row, column, name in frame_slots():
        path = source / name
        if not path.is_file():
            raise ValueError(f'missing frame: {name}')
        with Image.open(path) as cell:
            if cell.size != CELL:
                raise ValueError(f'{name}: expected {CELL[0]}x{CELL[1]}')
            # Paste without an alpha mask: copy every RGBA byte, including edge alpha.
            image.paste(cell.convert('RGBA'), (column * CELL[0], row * CELL[1]))
    errors = inspect_image(image)
    if errors:
        raise ValueError('; '.join(errors))
    destination.parent.mkdir(parents=True, exist_ok=True)
    image.save(destination, format='PNG')
    return validate(destination)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    check = commands.add_parser('validate', help='check dimensions, occupied cells and transparency')
    check.add_argument('source', type=Path)
    split = commands.add_parser('extract', help='export all 73 cells without changing their pixels')
    split.add_argument('source', type=Path)
    split.add_argument('--out', type=Path, required=True)
    merge = commands.add_parser('assemble', help='rebuild a PNG from exported cells')
    merge.add_argument('source', type=Path)
    merge.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.command == 'validate':
            result = validate(args.source)
        elif args.command == 'extract':
            result = extract(args.source, args.out)
        else:
            result = assemble(args.source, args.out)
    except (OSError, ValueError) as exc:
        parser.exit(2, f'error: {exc}\n')
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result['ok'] else 1


if __name__ == '__main__':
    sys.exit(main())
