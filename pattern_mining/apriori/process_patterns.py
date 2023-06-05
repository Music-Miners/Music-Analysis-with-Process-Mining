input_file = 'patterns.txt'
output_file = 'processedPatterns.txt'

patterns = {}

# Read the file
with open(input_file, 'r') as f:
    lines = f.readlines()
    # Iterate over the lines
    for line in lines:
        pattern_data = line.split(':')
        pattern = pattern_data[0]
        count = pattern_data[1]
        # Trim the pattern and change any whitespace to a single space
        pattern = pattern.strip()
        pattern = ' '.join(pattern.split())
        # Split the pattern into notes
        notes = pattern.split(' ')
        # Add the pattern to the dictionary
        patterns[pattern] = count

# Sort the patterns by split length (number of notes) and then by count
sorted_patterns = sorted(patterns.items(), key=lambda x: (len(x[0].split(' ')), x[1]), reverse=True)

# Write the patterns to the file
with open(output_file, 'w') as f:
    for pattern in sorted_patterns:
        f.write(pattern[0] + ':' + pattern[1])
