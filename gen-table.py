#!/usr/bin/env python3

import sys
import re
from collections import defaultdict

def parse_input(input_lines):
    engines = []
    current_engine = {}
    for line in input_lines:
        line = line.strip()
        if not line:
            continue
        if not current_engine:
            current_engine['name'] = line
            current_engine['benchmarks'] = {}
        elif line.startswith('---'):
            continue
        elif line.startswith('Score'):
            score = int(re.search(r'Score \(version 9\): (\d+)', line).group(1))
            current_engine['score'] = score
            engines.append(current_engine)
            current_engine = {}
        else:
            benchmark, value = line.split(':')
            current_engine['benchmarks'][benchmark.strip()] = int(value.strip())
    return engines

def generate_markdown_table(engines):
    all_benchmarks = sorted({benchmark for engine in engines for benchmark in engine['benchmarks']})
    header = ['Benchmark'] + [engine['name'] for engine in engines]
    rows = []

    for benchmark in all_benchmarks:
        row = [benchmark]
        for engine in engines:
            row.append(str(engine['benchmarks'].get(benchmark, '')))
        rows.append(row)

    # Add Score row
    score_row = ['Score']
    for engine in engines:
        score_row.append(str(engine['score']))
    rows.append(score_row)

    table = '|' + '|'.join(header) + '|\n'
    table += '|' + '|'.join(['-' * len(h) for h in header]) + '|\n'
    for row in rows:
        table += '|' + '|'.join(row) + '|\n'
    return table

def generate_ascii_table(engines):
    all_benchmarks = sorted({benchmark for engine in engines for benchmark in engine['benchmarks']})
    header = ['Benchmark'] + [engine['name'] for engine in engines]
    column_widths = [len(col) for col in header]

    for benchmark in all_benchmarks:
        column_widths[0] = max(column_widths[0], len(benchmark))
        for i, engine in enumerate(engines):
            column_widths[i+1] = max(column_widths[i+1], len(str(engine['benchmarks'].get(benchmark, ''))))

    column_widths[0] = max(column_widths[0], len('Score'))
    for i, engine in enumerate(engines):
        column_widths[i+1] = max(column_widths[i+1], len(str(engine['score'])))

    def format_row(row):
        return '| ' + ' | '.join(f"{str(item):<{column_widths[i]}}" for i, item in enumerate(row)) + ' |'

    table = format_row(header) + '\n'
    table += '+-' + '-+-'.join('-' * width for width in column_widths) + '-+\n'
    for benchmark in all_benchmarks:
        row = [benchmark]
        for engine in engines:
            row.append(str(engine['benchmarks'].get(benchmark, '')))
        table += format_row(row) + '\n'

    # Add Score row
    score_row = ['Score']
    for engine in engines:
        score_row.append(str(engine['score']))
    table += format_row(score_row) + '\n'

    return table

def main():
    if len(sys.argv) != 2 or sys.argv[1] not in ['ASCII', 'Markdown']:
        print("Usage: script.py [ASCII|Markdown]")
        return

    input_lines = sys.stdin.read().strip().split('\n')
    engines = parse_input(input_lines)

    if sys.argv[1] == 'Markdown':
        output = generate_markdown_table(engines)
    else:
        output = generate_ascii_table(engines)

    print(output)

if __name__ == '__main__':
    main()

