def split_hanford_file(input_file):
    output_files = ['out/aq_spec.dat', 'out/gases.dat', 'out/minerals.dat', 'out/srfcmplx.dat']
    chunks = []
    current_chunk = []

    with open(input_file, 'r') as file:
        for line in file:
            if line.strip().startswith("'null'"):
                if current_chunk:
                    chunks.append(current_chunk)
                    current_chunk = []
            else:
                current_chunk.append(line)
        # Add last chunk if file doesn't end with 'null'
        if current_chunk:
            chunks.append(current_chunk)

    # Skip the first chunk (as requested)
    relevant_chunks = chunks[1:]

    # Check we have exactly 4 chunks to write
    if len(relevant_chunks) != 4:
        raise ValueError(f"Expected 4 chunks after the first, but got {len(relevant_chunks)}")

    # Write each chunk to corresponding output file
    for output_file, chunk in zip(output_files, relevant_chunks):
        with open(output_file, 'w') as out_file:
            out_file.writelines(chunk)

    print("Splitting complete. Files created:", ', '.join(output_files))


# Run the function
if __name__ == '__main__':
    split_hanford_file('hanford.dat')
