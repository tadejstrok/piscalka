"""Make a `nuxt generate` build self-contained for static hosting.

The build is generated against a throwaway local API. This script copies the
uploaded media next to the pages and removes every reference to that API, so
the published site never makes requests to localhost.

Usage: finalize_static.py <public_dir> <media_dir>
"""

import shutil
import sys
from pathlib import Path

BS = chr(92)
API = "http://localhost:8000"
API_ESCAPED = "http:" + BS + "u002F" + BS + "u002Flocalhost:8000"
MEDIA = "/media"
MEDIA_ESCAPED = BS + "u002Fmedia"


def main(public_dir: Path, media_dir: Path) -> int:
    if media_dir.is_dir():
        shutil.copytree(media_dir, public_dir / "media", dirs_exist_ok=True)

    targets = [*public_dir.glob("*.html"), public_dir / "_payload.json"]
    for path in targets:
        text = path.read_text(encoding="utf-8")
        text = text.replace(API + MEDIA, MEDIA)
        text = text.replace(API_ESCAPED + MEDIA_ESCAPED, MEDIA_ESCAPED)
        text = text.replace(API, "").replace(API_ESCAPED, "")
        path.write_text(text, encoding="utf-8", newline="")

    leftovers = [p.name for p in targets if "localhost" in p.read_text(encoding="utf-8")]
    if leftovers:
        print(f"localhost still referenced in: {', '.join(leftovers)}")
        return 1

    print(f"Finalized {len(targets)} files")
    return 0


if __name__ == "__main__":
    sys.exit(main(Path(sys.argv[1]), Path(sys.argv[2])))
