"""一键生成所有 LeetCode 75 可视化动图"""
import subprocess, sys, os
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed

PROBLEMS_DIR = Path(__file__).parent / "problems"

def run_one(folder: Path):
    solution = folder / "solution.py"
    if not solution.exists():
        return (folder.name, None, "跳过 (无 solution.py)")
    try:
        result = subprocess.run(
            [sys.executable, str(solution)],
            capture_output=True, text=True, timeout=120,
            cwd=str(folder)
        )
        if result.returncode != 0:
            return (folder.name, False, result.stderr.strip()[-200:])
        return (folder.name, True, result.stdout.strip())
    except subprocess.TimeoutExpired:
        return (folder.name, False, "超时")

def main():
    folders = sorted(f for f in PROBLEMS_DIR.iterdir()
                     if f.is_dir() and f.name[:3].isdigit())
    print(f"共 {len(folders)} 题，开始生成...\n")

    ok, fail, skip = 0, 0, 0
    with ProcessPoolExecutor(max_workers=min(os.cpu_count() or 4, 8)) as ex:
        futures = {ex.submit(run_one, f): f for f in folders}
        for future in as_completed(futures):
            name, success, msg = future.result()
            if success is None:
                skip += 1
            elif success:
                ok += 1
                print(f"  ✓ {name}")
            else:
                fail += 1
                print(f"  ✗ {name}: {msg}")

    print(f"\n完成: {ok} 成功, {fail} 失败, {skip} 跳过")

if __name__ == "__main__":
    main()
