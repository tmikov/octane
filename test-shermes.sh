#!/bin/bash


if [ -z "$shermes" ]; then
shermes=/Users/tmikov/work/hws/sh-release/bin/shermes
fi

if [ "$1" = "list" ]; then
    for i in single/*.js; do 
        echo shermes -w $i -o b/$(basename "${i%.*}")
    done
fi

if [ -z "$1" ] || [ "$1" = "build" ]; then
    mkdir -p b

    $shermes -v -w single/box2d.js -o b/box2d
    $shermes -v -w single/crypto.js -o b/crypto
    $shermes -v -w single/deltablue.js -o b/deltablue
    $shermes -v -w single/earley-boyer.js -o b/earley-boyer
    $shermes -v -w single/gameboy.js -o b/gameboy
    #SLOW $shermes -v -w single/mandreel.js -o b/mandreel
    $shermes -v -w single/navier-stokes.js -o b/navier-stokes
    $shermes -v -w single/pdfjs.js -o b/pdfjs -Wc,-mllvm -Wc,-regalloc=basic
    $shermes -v -w single/raytrace.js -o b/raytrace
    $shermes -v -w single/regexp.js -o b/regexp
    $shermes -v -w single/richards.js -o b/richards
    $shermes -v -w single/splay.js -o b/splay
    $shermes -v -w single/typescript.js -o b/typescript
    $shermes -v -w single/zlib.js -o b/zlib
fi

if [ -z "$1" ] || [ "$1" = "run" ]; then
    for f in b/*; do
        ./$f
    done
fi
