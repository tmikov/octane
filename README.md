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

## Results

Results generated on Jul 1st, 2024.

|Benchmark|jsc --useJIT=0|v8 --jitless|hermes|sh-hermes|qjs|
|---------|--------------|------------|------|---------|---|
|Box2D|7531|5724|9172|9663|4544|
|Crypto|2049|1516|1718|1840|1259|
|DeltaBlue|1362|1343|1780|1753|1182|
|EarleyBoyer|5336|6891|5882|4979|2262|
|Gameboy|8151|9533|9855|10484|8926|
|Mandreel|1229|1401|1598|1650|1324|
|MandreelLatency|6294|9301|11675|11758|9643|
|NavierStokes|2775|2335|3239|3139|2637|
|PdfJS|11104|11516|7949|8136|4544|
|RayTrace|4042|4864|3307|3297|1303|
|RegExp|616|3384|800|778|275|
|Richards|1650|1405|1739|1947|1145|
|Splay|7815|8125|4449|5851|2424|
|SplayLatency|27036|25531|14827|18273|9857|
|Typescript|21560|25471|26064|25655|18104|
|zlib|2368|2517|2076|2230|3056|
|Score|4208|4812|4283|4461|2760|

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
