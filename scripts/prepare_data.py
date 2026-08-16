#!/usr/bin/env python3
"""
prepare_data.py - Downloads EuroSAT (RGB, Sentinel-2) and builds a balanced
two-class dataset:
    images_dataSAT/class_0_non_agri/  (non-agricultural land)
    images_dataSAT/class_1_agri/      (agricultural land)

Usage:
    python prepare_data.py [--max-per-class 3000] [--seed 42]
"""
import argparse
import os
import random
import shutil
import sys
import urllib.request
import zipfile

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
DOWNLOAD_ZIP = os.path.join(DATA_DIR, "EuroSAT_RGB.zip")
EXTRACT_DIR = os.path.join(DATA_DIR, "EuroSAT_RGB_extracted")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "images_dataSAT")

AGRI_CLASSES = ["AnnualCrop", "PermanentCrop", "Pasture"]
NON_AGRI_CLASSES = [
    "Forest",
    "HerbaceousVegetation",
    "Highway",
    "Industrial",
    "Residential",
    "River",
    "SeaLake",
]

SOURCES = [
    "https://zenodo.org/records/7711810/files/EuroSAT_RGB.zip",
    "https://zenodo.org/record/7711810/files/EuroSAT_RGB.zip",
    "https://madm.dfki.de/files/sentinel/EuroSAT.zip",
]


def download_file(url, dest):
    print(f"[download] {url}")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=120) as resp, open(dest, "wb") as out:
        shutil.copyfileobj(resp, out)
    print(f"[download] saved -> {dest} ({os.path.getsize(dest) / 1e6:.1f} MB)")


def ensure_zip():
    if os.path.exists(DOWNLOAD_ZIP):
        print(f"[zip] found existing archive: {DOWNLOAD_ZIP}")
        return
    last_err = None
    for url in SOURCES:
        try:
            download_file(url, DOWNLOAD_ZIP)
            with zipfile.ZipFile(DOWNLOAD_ZIP) as z:
                z.testzip()
            return
        except Exception as e:
            last_err = e
            print(f"[download] failed: {e}; trying next source...")
            if os.path.exists(DOWNLOAD_ZIP):
                os.remove(DOWNLOAD_ZIP)
    sys.exit(f"[error] all download sources failed. Last error: {last_err}")


def find_class_root():
    """Locate the folder containing the 10 EuroSAT class directories."""
    if not os.path.exists(EXTRACT_DIR):
        print(f"[extract] {DOWNLOAD_ZIP}")
        with zipfile.ZipFile(DOWNLOAD_ZIP) as z:
            z.extractall(EXTRACT_DIR)
    for root, dirs, files in os.walk(EXTRACT_DIR):
        names = set(dirs)
        if AGRI_CLASSES[0] in names and NON_AGRI_CLASSES[0] in names:
            return root
    sys.exit("[error] EuroSAT class folders not found after extraction")


def collect(root, classes):
    out = {}
    for cls in classes:
        d = os.path.join(root, cls)
        if not os.path.isdir(d):
            sys.exit(f"[error] missing class folder: {d}")
        out[cls] = sorted(
            os.path.join(d, f)
            for f in os.listdir(d)
            if f.lower().endswith((".jpg", ".jpeg", ".png"))
        )
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-per-class", type=int, default=3000)
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    random.seed(args.seed)
    os.makedirs(DATA_DIR, exist_ok=True)

    ensure_zip()
    class_root = find_class_root()
    print(f"[classes] found EuroSAT at: {class_root}")

    agri = collect(class_root, AGRI_CLASSES)
    non_agri = collect(class_root, NON_AGRI_CLASSES)

    agri_files = [f for cls in AGRI_CLASSES for f in agri[cls]]
    non_agri_pool = [f for cls in NON_AGRI_CLASSES for f in non_agri[cls]]
    random.shuffle(non_agri_pool)

    agri_selected = agri_files[: args.max_per_class]
    non_agri_selected = non_agri_pool[: len(agri_selected)]
    print(f"[data] agricultural images   : {len(agri_selected)}")
    print(f"[data] non-agricultural images: {len(non_agri_selected)}")

    targets = {
        "class_1_agri": agri_selected,
        "class_0_non_agri": non_agri_selected,
    }
    for folder, files in targets.items():
        dest_dir = os.path.join(OUTPUT_DIR, folder)
        os.makedirs(dest_dir, exist_ok=True)
        for i, src in enumerate(files):
            shutil.copy2(src, os.path.join(dest_dir, os.path.basename(src)))
        print(f"[done] {folder}: {len(files)} images -> {dest_dir}")


if __name__ == "__main__":
    main()
