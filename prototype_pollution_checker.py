#!/usr/bin/python3

import sys
import subprocess
import json

def extract_ast(js_file_path):
    try:
        result = subprocess.run(
            ["node", "parse_ast.js", js_file_path],
            capture_output=True, text=True, check=True
        )
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Node.js parse_ast.js failed:\n{e.stderr}")
        sys.exit(1)

def detect_proto_pollution(ast):
    findings = []

    def walk(node):
        if isinstance(node, dict):
            node_type = node.get('type')
            # Detect MemberExpression like obj['__proto__'] or obj.__proto__
            if node_type == "AssignmentExpression":
                left = node.get('left', {})
                if left.get('type') == "MemberExpression":
                    prop = left.get('property', {})
                    if (prop.get('type') == 'Literal' and prop.get('value') in ['__proto__', 'constructor', 'prototype']) \
                    or (prop.get('type') == 'Identifier' and prop.get('name') in ['__proto__', 'constructor', 'prototype']):
                        findings.append({
                            'line': prop.get('loc', {}).get('start', {}).get('line', '?'),
                            'property': prop.get('value') or prop.get('name'),
                            'code_snippet': f"{left.get('object', {}).get('name', 'obj')}.{prop.get('name') or prop.get('value')}"
                        })

            for key in node:
                walk(node[key])
        elif isinstance(node, list):
            for item in node:
                walk(item)

    walk(ast)
    return findings

def main():
    if len(sys.argv) != 2:
        print("Usage: python detect_proto_ast.py <target.js>")
        sys.exit(1)

    js_file = sys.argv[1]
    ast = extract_ast(js_file)
    results = detect_proto_pollution(ast)

    if results:
        print(f"[!] Prototype pollution risks detected in '{js_file}':\n")
        for finding in results:
            print(f"Line {finding['line']}: Access to '{finding['property']}' → {finding['code_snippet']}")
    else:
        print(f"[✓] No prototype pollution detected in '{js_file}'.")

if __name__ == "__main__":
    main()

