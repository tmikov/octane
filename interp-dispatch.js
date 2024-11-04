/**
 * Copyright (c) Meta Platforms, Inc. and affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */

// This benchmark is intended to reflect interpreter dispatch overhead,
// by berforming many, but very simple operations, no object access, no
// heap allocations, etc.

var InterpDispatch = new BenchmarkSuite('InterpDispatch', [50000], [
  new Benchmark("InterpDispatch", true, false, 0, runInterpDispatch)
]);

function InterDispatch_bench (lc, fc) {
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


function runInterpDispatch() {
    InterDispatch_bench(3000, 100);
}
