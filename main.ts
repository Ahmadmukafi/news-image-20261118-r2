import { execFileSync } from "node:child_process";
import { existsSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

// Entry point for news-image-20261118 (program/v1): draw the front page
// with draw.py and write it to /output/entry.png. No network is used.
// The grader mounts /output; locally, MAKEFUN_OUTPUT_DIR overrides it.
const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";
mkdirSync(outDir, { recursive: true });
execFileSync("python3", [join(here, "draw.py"), outDir],
  { stdio: "inherit" });
const out = join(outDir, "entry.png");
if (!existsSync(out)) {
  throw new Error("draw.py did not write entry.png");
}
console.log("wrote " + out);
