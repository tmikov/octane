/**
 * Copyright (c) Meta Platforms, Inc. and affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */

// This benchmark is intended to reflect interpreter dispatch overhead,
// by berforming many, but very simple operations, no object access, no
// heap allocations, etc.
//
// In this version we go one step further and allow the compiler to
// infer the types of the function parameters.

var InterpDispatch = new BenchmarkSuite('InterpDispatch2', [50000], [
  new Benchmark("InterpDispatch2", true, false, 0, runInterpDispatch2)
]);

function InterDispatch_bench2 (lc, fc) {
    lc = +lc;
    fc = +fc;
    var n, fact;
    var res = 0;
    while (--lc >= 0) {
        n = fc;
        fact = n;
        while (--n > 1)
            fact *= n;
        res += fact;
    }
    return res;
}


function runInterpDispatch2() {
    InterDispatch_bench2(3000, 100);
}
