#!/usr/bin/env python3

import os
import shutil
from pathlib import Path
from qbittorrentapi import Client

# Configuration
QBIT_HOST = os.getenv("QBIT_HOST")
QBIT_USERNAME = os.getenv("QBIT_USERNAME")
QBIT_PASSWORD = os.getenv("QBIT_PASS")

SOURCE_CATEGORY = os.getenv("SOURCE_CATEGORY")
DEST_CATEGORY = os.getenv("DEST_CATEGORY")

DOWNLOAD_ROOT = Path(os.getenv("DOWNLOAD_ROOT"))
IMPORT_ROOT = Path(os.getenv("IMPORT_ROOT"))


def copy_torrent_content(content_path: Path):
    dest_path = IMPORT_ROOT / content_path.name

    if dest_path.exists():
        print(f"Destination already exists, skipping copy: {dest_path}")
        return True

    print(f"Copying: {content_path} -> {dest_path}")

    try:
        if content_path.is_dir():
            shutil.copytree(content_path, dest_path)
        else:
            shutil.copy2(content_path, dest_path)
        return True
    except Exception as e:
        print(f"Failed to copy {content_path}: {e}")
        return False


def main():
    qb = Client(
        host=QBIT_HOST,
        username=QBIT_USERNAME,
        password=QBIT_PASSWORD,
    )

    qb.auth_log_in()
    print(qb.torrents_categories())
    torrents = qb.torrents_info(category=SOURCE_CATEGORY)

    print(f"Found {len(torrents)} torrents in category '{SOURCE_CATEGORY}'")

    for torrent in torrents:
        try:
            content_path = Path(torrent.content_path)
            print(content_path.name)
            # Some setups report paths outside the desired root.
            if not content_path.exists():
                # Try rebuilding from save_path + name
                content_path = Path(torrent.save_path) / torrent.name

            if not content_path.exists():
                print(
                    f"Cannot find content for '{torrent.name}' at "
                    f"{content_path}"
                )
                continue

            if copy_torrent_content(content_path):
                qb.torrents_set_category(
                    category=DEST_CATEGORY,
                    torrent_hashes=torrent.hash
                )

                print(
                    f"Updated category: "
                    f"{torrent.name} -> {DEST_CATEGORY}"
                )

        except Exception as e:
            print(f"Error processing {torrent.name}: {e}")

    print("Done.")


if __name__ == "__main__":
    main()