#!/usr/bin/env python3
"""打包 miaoyi-face 离线模型 v1.0 → GitHub release（CN-Miaos/miaoyi-face-models）。

幂等：已存在的 zip 不重打；release 已存在则 --clobber 覆盖同名资产。
源 = 真机上已验证跑通的那套（/storage/emulated/0/Android/data/com.miaos.miaoyi/files/models）。
"""
import hashlib
import json
import os
import subprocess
import sys
import time
import zipfile

ADB = os.environ.get("ADB", "adb")          # 例：D:/Android/Sdk/platform-tools/adb.exe
SERIAL = os.environ.get("ANDROID_SERIAL", "")   # 留空 = 唯一设备
DEV = "/storage/emulated/0/Android/data/com.miaos.miaoyi/files/models"
REPO = "CN-Miaos/miaoyi-face-models"
TAG = "v1.0"
APP_VERSION = "1.0.0"
ROOT = "D:/Hermes-project/miaoyi-face-models-release"
PULL = f"{ROOT}/pull"
OUT = f"{ROOT}/{TAG}"
BASE = f"https://github.com/{REPO}/releases/download/{TAG}/"

def L(zh, es, en):
    return {"zh": zh, "es": es, "en": en}

PKG = [
    dict(id="asr-zh", src="asr-zh", root="asr-zh", target="", stage=1,
         label=L("中文语音识别", "Voz (chino)", "Chinese ASR")),
    dict(id="asr-es", src="asr-es", root="asr-es", target="", stage=1,
         label=L("西语语音识别", "Voz (español)", "Spanish ASR")),
    dict(id="vad", src="vad", root="vad", target="", stage=1,
         label=L("人声检测", "Detección de voz", "Voice activity detection")),
    dict(id="denoise", src="denoise", root="denoise", target="", stage=1,
         label=L("语音降噪", "Reducción de ruido", "Speech denoising")),
    dict(id="mt-zh-en", src="mt/zh-en", root="zh-en", target="mt", stage=2,
         label=L("翻译 中→英", "Traducción zh→en", "MT zh→en")),
    dict(id="mt-en-es", src="mt/en-es", root="en-es", target="mt", stage=2,
         label=L("翻译 英→西", "Traducción en→es", "MT en→es")),
    dict(id="mt-es-zh", src="mt/es-zh", root="es-zh", target="mt", stage=2,
         label=L("翻译 西→中", "Traducción es→zh", "MT es→zh")),
    dict(id="tts-zh", src="tts/zh", root="zh", target="tts", stage=3,
         label=L("中文播报", "Voz sintética (chino)", "Chinese TTS")),
    dict(id="tts-es", src="tts/es", root="es", target="tts", stage=3,
         label=L("西语播报", "Voz sintética (español)", "Spanish TTS")),
]

STAGE_TITLE = {
    1: L("语音识别", "Reconocimiento de voz", "Speech recognition"),
    2: L("离线翻译", "Traducción sin conexión", "Offline translation"),
    3: L("语音播报", "Síntesis de voz", "Speech synthesis"),
}


def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def run(cmd, **kw):
    log("$ " + " ".join(cmd))
    p = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if p.returncode != 0:
        log(f"!! exit {p.returncode}\n{p.stdout[-2000:]}\n{p.stderr[-2000:]}")
        raise SystemExit(1)
    return p.stdout


def adb(*args):
    return run([ADB] + (["-s", SERIAL] if SERIAL else []) + list(args))


def device_files(rel):
    out = adb("shell", f"cd {DEV}/{rel} && find . -type f | wc -l")
    return int(out.strip())


def pull(src, dest):
    if os.path.isdir(dest) and os.listdir(dest):
        log(f"skip pull {src} (already local)")
        return
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    adb("pull", f"{DEV}/{src}", dest)


def make_zip(srcdir, arcname, outpath):
    if os.path.exists(outpath):
        log(f"skip zip {os.path.basename(outpath)}")
        return
    n = 0
    with zipfile.ZipFile(outpath, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        for root, _dirs, files in os.walk(srcdir):
            for f in sorted(files):
                full = os.path.join(root, f)
                rel = os.path.relpath(full, srcdir).replace("\\", "/")
                z.write(full, f"{arcname}/{rel}")
                n += 1
    log(f"zip {os.path.basename(outpath)}: {n} files -> {os.path.getsize(outpath)/1e6:.1f} MB")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def dir_bytes(path):
    total = 0
    for root, _d, files in os.walk(path):
        for f in files:
            total += os.path.getsize(os.path.join(root, f))
    return total


def main():
    os.makedirs(OUT, exist_ok=True)

    # 1) pull
    log("=== 1/5 从真机拉取模型 ===")
    for p in PKG:
        dest = os.path.join(PULL, p["src"])
        pull(p["src"], dest)
        dcount = device_files(p["src"])
        lcount = sum(len(fs) for _r, _d, fs in os.walk(dest))
        assert dcount == lcount == dcount, f"{p['id']} file count mismatch: device={dcount} local={lcount}"
        log(f"  {p['id']}: {lcount} files ok")

    # 2) zip
    log("=== 2/5 打包 ===")
    for p in PKG:
        make_zip(os.path.join(PULL, p["src"]), p["root"], os.path.join(OUT, f"{p['id']}.zip"))

    # 3) hashes + manifest
    log("=== 3/5 计算 sha256 与清单 ===")
    stages = {}
    total_dl = total_up = 0
    for p in PKG:
        zp = os.path.join(OUT, f"{p['id']}.zip")
        entry = {
            "id": p["id"],
            "label": p["label"],
            "file": f"{p['id']}.zip",
            "url": BASE + f"{p['id']}.zip",
            "target": p["target"],
            "bytes": os.path.getsize(zp),
            "unpacked_bytes": dir_bytes(os.path.join(PULL, p["src"])),
            "sha256": sha256(zp),
            "files": sum(len(fs) for _r, _d, fs in os.walk(os.path.join(PULL, p["src"]))),
        }
        total_dl += entry["bytes"]
        total_up += entry["unpacked_bytes"]
        s = stages.setdefault(p["stage"], {"stage": p["stage"], "title": STAGE_TITLE[p["stage"]],
                                           "download_bytes": 0, "packages": []})
        s["download_bytes"] += entry["bytes"]
        s["packages"].append(entry)
        log(f"  {entry['id']}: {entry['bytes']/1e6:.1f} MB packed / {entry['unpacked_bytes']/1e6:.1f} MB unpacked  {entry['sha256'][:16]}…")

    manifest = {
        "schema": 1,
        "app": "miaoyi-face",
        "version": APP_VERSION,
        "release_tag": TAG,
        "base_url": BASE,
        "models_dir": "models",
        "total_download_bytes": total_dl,
        "total_unpacked_bytes": total_up,
        "stages": [stages[k] for k in sorted(stages)],
    }
    mpath = os.path.join(OUT, "models.json")
    with open(mpath, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
        f.write("\n")
    log(f"清单: {mpath}  总下载 {total_dl/1e6:.1f} MB / 解包 {total_up/1e6:.1f} MB")

    # 4) release
    log("=== 4/5 建 release 并上传 ===")
    notes = os.path.join(ROOT, "release-notes.md")
    run(["gh", "release", "create", TAG, "--repo", REPO,
         "--title", f"miaoyi-face 模型包 {TAG}", "--notes-file", notes, "--latest"])
    run(["gh", "release", "upload", TAG, mpath, "--repo", REPO, "--clobber"])
    log("  清单已上线")
    for p in PKG:
        zp = os.path.join(OUT, f"{p['id']}.zip")
        run(["gh", "release", "upload", TAG, zp, "--repo", REPO, "--clobber"])
        log(f"  上传完成 {p['id']}")

    # 5) 资产复核
    log("=== 5/5 线上资产复核 ===")
    out = run(["gh", "release", "view", TAG, "--repo", REPO, "--json", "assets",
               "--jq", ".assets[] | \"\\(.name) \\(.size)\""])
    print(out)
    expected = {f"{p['id']}.zip" for p in PKG} | {"models.json"}
    got = {line.split()[0] for line in out.strip().splitlines()}
    missing = expected - got
    assert not missing, f"线上缺资产: {missing}"
    log("全部资产就位 ✓")


if __name__ == "__main__":
    main()
