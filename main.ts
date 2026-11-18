// ONE DAY - news-image-20261118 round 2 entry point.
// Copies the pre-rendered entry.png beside this file into the output
// directory ($MAKEFUN_OUTPUT_DIR, default /output). No python, no
// network, no timestamps: the output is byte-identical every run.
import { copyFileSync, existsSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });

const here = dirname(fileURLToPath(import.meta.url));
const src = join(here, "entry.png");
if (!existsSync(src)) {
  throw new Error("entry.png missing from the repository");
}

copyFileSync(src, join(outDir, "entry.png"));
console.log("wrote entry.png to " + outDir);
