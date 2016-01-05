__author__ = 'Evan Downing'

import sys
import os
import datetime
import random


# Extracts words from file
def extract_words(fn):
    with open(fn, 'r') as fr:

        final_words = list()

        # Get each line in the file
        for line in fr:
            # Split the line into words
            words = line.split(' ')

            # Store words in list
            for w in words:
                if w:
                    final_words.append(w)

        # Return words
        return final_words


# Extracts characters from file
def extract_chars(fn):
    with open(fn, 'r') as fr:

        final_chars = list()

        # Get each line in the file
        for line in fr:
            # Split the line into chars
            chars = list(line)

            # Store words in list
            for c in chars:
                final_chars.append(c)

        # Return chars
        return final_chars


# Create Markov chain
def create_chain(chain, chainSize, tokens):
    # Store token chain and following token into Markov chain
    for index in range(len(tokens) - chainSize):

        group = tuple(tokens[index:index+chainSize])
        nextToken = tokens[index+chainSize]

        # If the token chain does not already exist in the chain, add it
        if group not in chain:
            chain[group] = list()

        # Add next word to group
        chain[group].append(nextToken)


# Generates lines composed of Markov text
def generate_lines(chain, n, separation):
    # Randomly select a starting point that doesn't contain a newline
    group = list(random.choice(chain.keys()))

    count = 0

    # Construct beginning of line
    lines = ''
    for t in group:

        # Count how many newlines are present in the token
        if '\n' in t:
            count += 1

        # Add chain's token to line
        lines += '{0}'.format(t)

        # Add separation character to line
        lines += separation

    # Construct rest of lines
    while (1):
        # If the chain does not exist in the Markov chain, continue in
        # the loop with a new random seed

        # This probably means the chain is a chain in the last
        # line of a document and as no other values after it.
        if tuple(group) not in chain:
            group = list(random.choice(chain.keys()))

            for t in group:

                # Count how many newlines are present in the token
                if '\n' in t:
                    count += 1

                # Add chain's token to line
                lines += '{0}'.format(t)

                # Add separation character to line
                lines += separation

        # Find next token in line
        nextToken = random.choice(chain[tuple(group)])

        # Update lines with next token
        lines += nextToken

        # If this token contains a newline character, increment count
        flag = False
        if '\n' in nextToken:
            count += 1
            flag = True

        # If the total number of lines has been reached,
        # quit constructing lines
        if count == n:
            break

        # Update line with a separation character
        # if line didn't end in a newline
        if not flag:
            lines += separation

        # Update token chain
        group.append(nextToken)
        group.pop(0)

    # Output generated lines
    sys.stdout.write('{0}'.format(lines))


# Get list of files in "path"
# Path can be either a single file or a folder of folders/files
def get_path_files(path):

    # If path does not exist, return error
    if not os.path.exists(path):
        print 'Error: {0} does not exist.'.format(path)
        sys.exit(1)

    # If path is a file, return the filename
    if os.path.isfile(path):
        yield path

    # Else if path is a directory, return all filenames in directory
    # and child directories
    else:
        for root, dirs, files in os.walk(path):
            for fn in files:
                yield os.path.join(root, fn)


def _main():
    if len(sys.argv) != 5:
        print 'usage: python markov.py type input chain-size number-of-lines'
        print ''
        print '\ttype: \'words\' or \'chars\''
        print '\tinput: file/folder name'
        print '\tchain-size: integer'
        print '\tnumber-of-lines: integer'
        print ''
        sys.exit(2)

    typeName = sys.argv[1]
    inputName = sys.argv[2]
    chainSize = int(sys.argv[3])
    numLines = int(sys.argv[4])

    if (typeName != 'words') and (typeName != 'chars'):
        print 'Type should be either \'words\' or \'chars\'.'
        sys.exit(2)

    # Define variable to store Markov chain
    chain = dict()

    # Get files in input folder
    paths = get_path_files(inputName)

    # Collect tokens (words or chars) in files
    allTokens = list()

    # Input data from files
    for fn in paths:
        # Display status
        print datetime.datetime.now(), '\t', 'Parsing file: {0}'.format(fn)

        # Get words in file
        if typeName == 'words':
            tokens = extract_words(fn)
        # Get characters in file
        elif typeName == 'chars':
            tokens = extract_chars(fn)

        allTokens.extend(tokens)

        # If size requested is longer or equal to the length of the words, quit
        if chainSize >= len(tokens):
            if typeName == 'words':
                print 'Error: chain-size is greater than or equal'\
                      ' to the number of words in file.'
            elif typeName == 'chars':
                print 'Error: chain-size is greater than or equal'\
                      ' to the number of characters in file.'

            sys.exit(1)

        # Put tokens into chain
        create_chain(chain, chainSize, tokens)

    # Sanity-check input for newline characters
    flag = False
    for w in allTokens:
        # If word contains line-terminating character
        if '\n' in w:
            flag = True
            break

    if not flag:
        print 'Error: Input does not contain at least one newline.'
        sys.exit(1)

    # Display status
    print datetime.datetime.now(), '\t', 'Generating Markov text'

    # Generate text
    if typeName == 'words':
        generate_lines(chain, numLines, ' ')
    elif typeName == 'chars':
        generate_lines(chain, numLines, '')


if __name__ == '__main__':
    _main()
