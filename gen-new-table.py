#!/usr/bin/env python3

import sys

def parse_benchmark_data(file_content):
    """
    Parses the input benchmark data from the provided text content.
    Returns a dictionary with keys as engine invocations and values as dictionaries
    of benchmark names and their respective results.
    """
    results = {}
    current_engine = ""
    current_benchmarks = {}

    # Split by lines to process each individually
    lines = file_content.strip().splitlines()

    for line in lines:
        # Check if it's an engine invocation line
        if line.startswith("$ "):
            # Save the previous engine's benchmarks if they exist
            if current_engine and current_benchmarks:
                results[current_engine] = current_benchmarks
                current_benchmarks = {}
            current_engine = line.strip()
        # Check for score line and add it as a "Score" benchmark
        elif line.startswith("Score"):
            score_value = line.split(":")[1].strip()
            current_benchmarks["Score"] = score_value
        # Regular benchmark line
        elif ":" in line:
            benchmark_name, result_value = line.split(":", 1)
            current_benchmarks[benchmark_name.strip()] = result_value.strip()

    # Add the last parsed engine's benchmarks
    if current_engine and current_benchmarks:
        results[current_engine] = current_benchmarks

    return results


def format_ascii_table(results, relative=False):
    """
    Formats the parsed benchmark results into an ASCII table.
    If 'relative' is True, each value is calculated as a ratio relative to the first entry in each row.
    """
    # Extract unique engine invocations and benchmark names
    engine_invocations = list(results.keys())
    benchmark_names = list(next(iter(results.values())).keys())

    # Number the engine invocations
    engine_labels = {engine: idx + 1 for idx, engine in enumerate(engine_invocations)}

    # Calculate column widths for each engine, depending on whether we display absolute or relative values
    column_widths = {}
    for engine in engine_invocations:
        max_width = max(
            len(f"{(float(results[engine].get(benchmark, '1')) / float(results[engine_invocations[0]].get(benchmark, '1'))):.2f}")
            if relative and float(results[engine_invocations[0]].get(benchmark, "1")) != 0 else len(results[engine].get(benchmark, ""))
            for benchmark in benchmark_names
        )
        column_widths[engine] = max(max_width, len(str(engine_labels[engine])))  # Ensure it fits the label too

    # Add padding for readability in each column
    column_padding = 2  # Padding around each entry
    padded_column_widths = {engine: width + column_padding for engine, width in column_widths.items()}

    # Build the header row with fixed width for each engine column
    header_row = " | ".join(f"{engine_labels[engine]:^{padded_column_widths[engine]}}" for engine in engine_invocations)
    header_border = "-" * (len(header_row) + len(benchmark_names[0]) + 5)

    # Start building the output
    output = []
    table_title = "Ratio Table (relative to first entry in each row)" if relative else "Absolute Table"
    output.append(f"\n{table_title}")
    output.append("\nEngine Invocations:")
    for engine, label in engine_labels.items():
        output.append(f"{label}: {engine}")
    output.append("\n" + header_border)
    output.append(f"| {' ' * 15} | {header_row} |")
    output.append(header_border)

    # Add each benchmark row with properly formatted values
    for benchmark in benchmark_names:
        row = " | ".join(
            f"{(float(results[engine].get(benchmark, '0')) / float(results[engine_invocations[0]].get(benchmark, '1'))):.2f}"
            if relative and float(results[engine_invocations[0]].get(benchmark, "1")) != 0
            else results[engine].get(benchmark, '').rjust(padded_column_widths[engine])
            for engine in engine_invocations
        )
        output.append(f"| {benchmark.ljust(15)} | {row} |")

    output.append(header_border)
    return "\n".join(output)


# Main function to generate both absolute and ratio tables
def main():
    # Read the entire content from stdin
    file_content = sys.stdin.read()
    results = parse_benchmark_data(file_content)

    # Generate the absolute and ratio tables
    absolute_table = format_ascii_table(results, relative=False)
    ratio_table = format_ascii_table(results, relative=True)

    # Output both tables to stdout
    print(absolute_table)
    print("\n\n" + ratio_table)

# Updating this to use in the script if executed directly
if __name__ == "__main__":
    main()

