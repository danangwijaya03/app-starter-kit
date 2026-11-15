#!/usr/bin/env python3
"""Apply narrowly scoped architecture-v2 documentation consistency changes.

Zero-guess policy: every replacement must match a known original anchor or an
already-applied replacement. No files are written if any anchor is unexpected.
Only doc files; TASKS.yaml and source code are never modified.
"""
from __future__ import annotations

import argparse
import datetime as dt
import difflib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
MANIFEST = HERE / "patches.json"

def fail(msg: str) -> None:
    print("ERROR:", msg, file=sys.stderr)
    raise SystemExit(2)

def git_status(repo: Path, relpaths: list[str], *, allow_dirty: bool = False) -> None:
    if not (repo / ".git").exists():
        fail(f"{repo} bukan checkout Git (folder .git tidak ditemukan).")
    dirty = []
    for relpath in relpaths:
        p = subprocess.run(
            ["git", "-C", str(repo), "status", "--porcelain", "--", relpath],
            capture_output=True, text=True, check=True,
        )
        if p.stdout.strip():
            dirty.append(relpath)
    if dirty and not allow_dirty:
        fail(
            "Ada perubahan lokal pada dokumen target:\n- " + "\n- ".join(dirty)
            + "\nPerubahan tidak ditimpa. Periksa diff, lalu gunakan --apply --allow-dirty "
              "hanya jika ingin menggabungkan anchor yang cocok ke file lokal tersebut."
        )
    if dirty and allow_dirty:
        print(
            "PERINGATAN: Menerapkan patch ke file yang memiliki perubahan lokal. "
            "Semua anchor akan divalidasi dan salinan lengkap dibuat sebelum menulis."
        )


def count_tasks(text: str) -> int:
    return len(re.findall(r"(?m)^\s*-\s+id:\s+P\d{2}-\d{2}[A-Z]?\s*$", text))

def guard_registry(repo: Path, manifest: dict) -> None:
    task_file = repo / "docs/agent/TASKS.yaml"
    if not task_file.is_file():
        fail("docs/agent/TASKS.yaml tidak ditemukan.")
    tasks = task_file.read_text(encoding="utf-8")
    expected = manifest["task_registry_expected"]
    actual = count_tasks(tasks)
    if actual != expected or not re.search(r"(?m)^\s*task_count:\s*162\s*$", tasks):
        fail(f"Task registry berubah: hitung={actual}, expected={expected}, metadata wajib 162. Paket harus diperiksa ulang.")
    adr_dir = repo / "docs/architecture/ADR"
    adrs = list(adr_dir.glob("ADR-[0-9][0-9][0-9]-*.md"))
    expected_adrs = manifest["adrs_expected"]
    if len(adrs) != expected_adrs:
        fail(f"ADR berjumlah {len(adrs)} bukan {expected_adrs}. Audit perubahan repository dahulu.")

def transformed(source: str, replacements: list[dict], relpath: str) -> tuple[str, int, int]:
    result = source
    changed = already = 0
    for idx, step in enumerate(replacements, 1):
        before, after = step["from"], step["to"]
        if not before or before == after:
            fail(f"Patch {relpath}#{idx} invalid (empty/identical).")
        a, b = result.count(before), result.count(after)
        if a == 1 and b == 0:
            result = result.replace(before, after, 1)
            changed += 1
        elif a == 0 and b == 1:
            already += 1
        else:
            fail(f"Anchor tidak cocok / ambigu untuk {relpath}#{idx}: old={a}, new={b}. "
                 "Repo mungkin berubah; jangan paksa replace.")
    return result, changed, already

def build_plan(repo: Path, manifest: dict):
    outputs = {}
    counter_changed = counter_already = 0
    for file_plan in manifest["file_changes"]:
        relpath = file_plan["path"]
        if Path(relpath).is_absolute() or ".." in Path(relpath).parts:
            fail(f"Path tidak aman: {relpath}")
        target = repo / relpath
        if not target.is_file() or target.is_symlink():
            fail(f"Dokumen harus file biasa dan sudah ada: {relpath}")
        raw = target.read_bytes()
        if b"\r\n" in raw:
            fail(f"{relpath} menggunakan CRLF; normalisasi dengan review terpisah, bukan patch otomatis.")
        original = raw.decode("utf-8")
        updated, changed, already = transformed(original, file_plan["replacements"], relpath)
        outputs[relpath] = (original, updated, changed, already)
        counter_changed += changed
        counter_already += already
    return outputs, counter_changed, counter_already

def backup_dir_for(repo: Path) -> Path:
    ts = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    base = repo.parent / f"{repo.name}.arch-v2-sync-backup-{ts}"
    dest = base
    n = 1
    while dest.exists():
        dest = Path(str(base) + f"-{n}")
        n += 1
    return dest

def atomic_write(path: Path, content: str) -> None:
    stat = path.stat()
    fd, tmp_name = tempfile.mkstemp(prefix=".v2-sync-", suffix=".tmp", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as f:
            f.write(content)
            f.flush()
            os.fsync(f.fileno())
        os.chmod(tmp_name, stat.st_mode)
        os.replace(tmp_name, path)
    except BaseException:
        if Path(tmp_name).exists():
            Path(tmp_name).unlink()
        raise

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=".", help="Lokasi root checkout app-starter-kit")
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--apply", action="store_true", help="Buat backup lalu ubah dokumen")
    modes.add_argument("--check", action="store_true", help="Wajibkan semua 32 patch sudah diterapkan")
    modes.add_argument("--export", action="store_true", help="Buat file lengkap hasil revisi di folder terpisah (tanpa mengubah repo)")
    parser.add_argument("--show-diff", action="store_true", help="Cetak perubahan (tanpa menulis)")
    parser.add_argument(
        "--allow-dirty", action="store_true",
        help="Izinkan --apply untuk file dengan perubahan Git lokal, setelah anchor check dan backup; tidak berlaku pada mode lain"
    )
    args = parser.parse_args()
    if args.allow_dirty and not args.apply:
        fail("--allow-dirty hanya boleh digunakan bersama --apply.")
    repo = Path(args.repo).resolve()
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    relpaths = [f["path"] for f in manifest["file_changes"]]
    guard_registry(repo, manifest)
    outputs, changed, already = build_plan(repo, manifest)
    if args.apply and changed:
        git_status(repo, relpaths, allow_dirty=args.allow_dirty)
    print(f"Patch: {changed} belum diterapkan; {already} sudah diterapkan; target: {len(outputs)} dokumen.")
    if args.show_diff or (not args.apply and not args.check):
        for path, (original, updated, count, _) in outputs.items():
            if not count:
                continue
            print("".join(difflib.unified_diff(
                original.splitlines(keepends=True), updated.splitlines(keepends=True),
                fromfile="a/" + path, tofile="b/" + path,
            )))
    if args.export:
        dest = repo.parent / (repo.name + ".architecture-v2-replacement-files")
        if dest.exists():
            fail(f"Folder export sudah ada: {dest}. Pindahkan/hapus secara manual dahulu agar tidak menimpa data.")
        for relpath, (_, updated, _, _) in outputs.items():
            exported = dest / relpath
            exported.parent.mkdir(parents=True, exist_ok=True)
            exported.write_text(updated, encoding="utf-8", newline="\n")
        print(f"EXPORTED: {len(outputs)} file pengganti lengkap ke {dest}")
        print("Review diff dulu. Salin file-file dari folder ini ke path yang sama dalam repository hanya setelah diverifikasi.")
        return
    if args.check:
        if changed:
            fail(f"{changed} patch masih pending. Jalankan --apply setelah review diff.")
        print("PASS: seluruh anchor revisi hadir; task ID 162 dan ADR 16 dipertahankan.")
        return
    if args.apply:
        changed_files = [(p, o, u) for p,(o,u,c,_) in outputs.items() if c]
        if not changed_files:
            print("Tidak ada perubahan. Sudah sinkron.")
            return
        backup = backup_dir_for(repo)
        backup.mkdir(parents=True)
        for path, original, _ in changed_files:
            b = backup / path
            b.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(repo / path, b)
        (backup / "README.txt").write_text(
            "Backup dibuat sebelum apply Architecture v2 consistency sync.\n"
            "Salin file dari folder ini kembali ke lokasi sama bila perlu rollback.\n"
            "Tidak ada migrasi database, task registry, atau source code yang diubah.\n",
            encoding="utf-8"
        )
        try:
            for path, original, updated in changed_files:
                atomic_write(repo / path, updated)
        except BaseException:
            print("Penerapan gagal; lakukan restore manual dari:", backup, file=sys.stderr)
            raise
        print(f"APPLIED: {len(changed_files)} file. Backup: {backup}")
        print("Verifikasi: git diff --check && git diff -- docs")
        print("Lalu jalankan python3 tools/architecture_v2_sync/apply.py --repo . --check")

if __name__ == "__main__":
    main()
