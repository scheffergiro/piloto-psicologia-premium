#!/usr/bin/env python3
"""Compatibilidade de importação; a única implementação oficial está em gerar.py."""
from gerar import gerar


def gerar_retrato(config_path, output_path, experimental=True):
    # No alternate renderer or visual direction.
    gerar(config_path, output_path, experimental=experimental)


if __name__ == '__main__':
    raise SystemExit('Use python3 gerar.py --config cliente.json --output public')
