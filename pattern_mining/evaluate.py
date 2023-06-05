import sys
 
folder = sys.argv[1]
input_file = folder + '/processedLogs.csv'
output_file = folder + '/results.txt'

pairs = {
    1: [14],
    2: [11],
    3: [15],
    4: [12],
    5: [],
    6: [13, 16],
    7: [17],
    8: [18],
    9: [19],
    10: [20],
    11: [2],
    12: [4],
    13: [6, 16],
    14: [1],
    15: [3],
    16: [6, 13],
    17: [7],
    18: [8],
    19: [9],
    20: [10]
}

correctCount = 0

# Open the output file
file = open(output_file, 'w')

# Read the file
with open(input_file, 'r') as f:
    lines = f.readlines()
    # Iterate over the lines
    for index, line in enumerate(lines):
        allCorrect = True
        for pair in pairs[index + 1]:
            if lines[pair - 1] != line:
                print('====================')
                print('Error: line ' + str(index + 1) + ' does not match line ' + str(pair) + '.')
                print('Line ' + str(index + 1) + ': ' + line)
                print('Line ' + str(pair) + ': ' + lines[pair - 1])
                print('====================')
                allCorrect = False
                file.write('====================\n')
                file.write('Error: line ' + str(index + 1) + ' does not match line ' + str(pair) + '.\n')
                file.write('Line ' + str(index + 1) + ': ' + line)
                file.write('Line ' + str(pair) + ': ' + lines[pair - 1])
                file.write('====================\n')
        if allCorrect:
            correctCount += 1

# Print the results
if correctCount == len(lines):
    print('All lines match.')
    file.write('All lines match.\n')
else:
    print('Not all lines match.')
    file.write('Not all lines match.\n')
print(str(correctCount) + ' lines match.')
file.write(str(correctCount) + ' lines match.\n')

# Close the file
file.close()
