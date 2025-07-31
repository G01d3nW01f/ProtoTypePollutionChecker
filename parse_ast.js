// parse_ast.js
const espree = require('espree');
const fs = require('fs');

const file = process.argv[2];
const code = fs.readFileSync(file, 'utf-8');

try {
    const ast = espree.parse(code, {
        ecmaVersion: "latest",
        sourceType: "module", // または 'script' でも可
        loc: true,
        range: true,
        tokens: true,
        comment: true
    });

    console.log(JSON.stringify(ast, null, 2));
} catch (err) {
    console.error("[ESPREE PARSE ERROR]:", err.message);
    process.exit(1);
}

