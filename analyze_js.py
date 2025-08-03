#!/usr/bin/env python3

import re
import sys
import os

def extract_info(js_code):
    result = {}

    # 関数一覧
    functions = re.findall(r'function\s+([a-zA-Z0-9_$]+)\s*\(|([a-zA-Z0-9_$]+)\s*=\s*\(.*?\)\s*=>', js_code)
    result['functions'] = list(set([f[0] or f[1] for f in functions if f[0] or f[1]]))

    # eval系
    result['eval_usage'] = re.findall(r'\b(eval|Function|setTimeout|setInterval)\s*\(', js_code)

    # DOMアクセス
    result['dom_access'] = re.findall(r'document\.(getElementById|getElementsByClassName|querySelector|write|createElement)', js_code)

    # 外部通信
    result['network_calls'] = re.findall(r'\b(fetch|XMLHttpRequest|axios|navigator\.sendBeacon)\b', js_code)

    # グローバル変数っぽい検出（簡易）
    result['potential_globals'] = re.findall(r'^[ \t]*([a-zA-Z0-9_$]+)\s*=\s*', js_code, re.MULTILINE)

    return result

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 analyze_js.py path/to/file.js")
        sys.exit(1)

    path = sys.argv[1]

    if not os.path.isfile(path) or not path.endswith('.js'):
        print("Error: Must provide a valid .js file")
        sys.exit(1)

    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        js_code = f.read()

    info = extract_info(js_code)

    print("\n===== JavaScript Analysis Report =====")
    print(f"Analyzing file: {path}\n")

    print("🔹 Functions Defined:")
    for fn in info['functions']:
        print(f"  - {fn}")

    print("\n🔹 Use of eval/Function/setTimeout/setInterval:")
    for item in info['eval_usage']:
        print(f"  - {item}")

    print("\n🔹 DOM Access Methods:")
    for dom in info['dom_access']:
        print(f"  - document.{dom}")

    print("\n🔹 External Network Requests:")
    for net in info['network_calls']:
        print(f"  - {net}")

    print("\n🔹 Potential Global Variable Assignments:")
    for gvar in info['potential_globals']:
        print(f"  - {gvar}")

    print("\n=======================================\n")

if __name__ == "__main__":
    main()

