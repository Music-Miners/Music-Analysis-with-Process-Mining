logs_file = 'logs.csv'
patterns_file = 'processedPatterns.txt'
output_file = 'processedLogs.csv'
min_pattern_length = 2

# Read the patterns file
patterns = []
with open(patterns_file, 'r') as f:
    lines = f.readlines()
    # Iterate over the lines
    for line in lines:
        pattern_data = line.split(':')
        pattern = pattern_data[0]
        count = pattern_data[1]
        # Split the pattern into notes
        notes = pattern.split(' ')
        # Add notes to the patterns list
        patterns.append(notes)

# Open the output file
file = open(output_file, 'w')

def match_pattern(pattern_list, actual_list):
    if len(pattern_list) > len(actual_list):
        return False

    index_b = 0
    for element in pattern_list:
        while index_b < len(actual_list) and actual_list[index_b] != element:
            index_b += 1

        if index_b >= len(actual_list):
            return False

        index_b += 1

    return True

# Read the logs file
with open(logs_file, 'r') as f:
    lines = f.readlines()
    # Iterate over the lines
    for line in lines:
        # Trim the log and change any whitespace to a single space
        log = line.strip()
        log = ' '.join(log.split())
        # Split the log into notes
        notes = log.split(' ')
        # Iterate over the patterns
        pattern_found = False
        for pattern in patterns:
            # Check if the pattern is shorter than the minimum pattern length
            if len(pattern) < min_pattern_length:
                break
            # Check if the pattern is in the log
            # TODO: actually check if the pattern is a subset of the log
            ###if match_pattern(pattern, notes):
            if set(pattern).issubset(set(notes)): # stub set check
                # Write the pattern to the file
                file.write(' '.join(pattern) + '\n')
                pattern_found = True
                break
        # Write the notes to the file
        if not pattern_found:
            file.write(' '.join(notes) + '\n')

# Close the output file
file.close()
