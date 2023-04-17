from pathlib import Path


def get() -> str:
    return open(Path(__file__).parent/'top_layout.html', 'r', encoding='utf-8').read()
