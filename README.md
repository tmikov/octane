# Octane

Fork of Octane (https://github.com/chromium/octane), tweaked for easy
usage with Hermes.

## TLDR

To run the benchmark with Hermes, it must first be generated. From the project
directory,
execute:

```shell
./gen-full.py run-noeval.js gen-noeval.js .
```

Then use various engines to run the generated benchmark:
```shell
jsc --useJIT=0 gen-noeval.js
hermes -w gen-noeval.js
```

## Detailed Changes

### run-noeval.js

The original benchmark [run.js](run.js) loads a benchmark (code-load.js)
[code-load.js] relying on `eval()`. That doesn't make sense for Hermes, so
it was removed in a new version of the file: [run-noeval.js](run-noeval.js).

### zlib-data-1.js

The original zlib benchmark's code is entirely contained in a single string
that is then passed to eval in [zlib-data.js](zlib-data.js). For Hermes, the
following transformations was applied:
1. Get the body of the benchmark by replacing `eval()` with `print
   ()`.
2. Apply prettier.
3. Expose a dummy function `read()`, which isn't used but is referred to.

### gen-full.py

The original benchmark [run.js](run.js) uses `load(filename)` to load the
individual benchmarks. `load()` does not make sense for Hermes; instead a
simple script [gen-full.py](gen-full.py) replaces each `load()` with the
contents of the loaded file. The invocation is:

```shell
./gen-full.py input.js output.js project-dir
```
