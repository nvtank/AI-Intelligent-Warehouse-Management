// TypeScript handles types/unused symbols; ESLint checks transpiled JS semantics.
// This avoids adding a TypeScript parser/plugin outside the approved packages.
import { readdir, readFile } from "node:fs/promises";
import { join, relative } from "node:path";
import { fileURLToPath } from "node:url";
import { ESLint } from "eslint";
import ts from "typescript";

const root = fileURLToPath(new URL("../", import.meta.url));
const eslint = new ESLint({ cwd: root });

async function sourceFiles(directory) {
  const files = [];
  for (const entry of await readdir(directory, { withFileTypes: true })) {
    const path = join(directory, entry.name);
    if (entry.isDirectory()) files.push(...await sourceFiles(path));
    else if (/\.tsx?$/.test(entry.name) && !entry.name.endsWith(".d.ts")) files.push(path);
  }
  return files;
}

const results = [];
for (const path of await sourceFiles(join(root, "apps/web/src"))) {
  const source = await readFile(path, "utf8");
  const { outputText } = ts.transpileModule(source, {
    fileName: path,
    compilerOptions: {
      target: ts.ScriptTarget.ES2022,
      module: ts.ModuleKind.ESNext,
      jsx: ts.JsxEmit.ReactJSX,
    },
  });
  const filePath = path.replace(/\.tsx?$/, ".js");
  const linted = await eslint.lintText(outputText, { filePath });
  // Diagnostics refer to emitted JavaScript; TypeScript reports source errors.
  for (const result of linted) result.filePath = `${relative(root, path)} (emitted JS)`;
  results.push(...linted);
}
results.push(...await eslint.lintFiles([
  join(root, "eslint.config.mjs"),
  join(root, "scripts/*.mjs"),
  join(root, "apps/web/vite.config.mjs"),
]));
const formatter = await eslint.loadFormatter("stylish");
const output = formatter.format(results);
if (output) process.stdout.write(output);
if (results.some((result) => result.errorCount || result.warningCount)) process.exitCode = 1;
else process.stdout.write(`ESLint passed for ${results.length} files.\n`);
