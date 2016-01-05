# Markov Text Generator

My implementation of a Markov text generator.

## Features:
* type: Can either be 'words' or 'chars'. This is to say that the Markov chain will be created by words (characters separated by a space) or by characters alone.
* input: Can either be a single file's name or a folder's name which includes folders and files inside of it. This program will follow all subdirectories if a directory is given.
* chain-size: Size (integer) of chain of tokens used as the seed in the Markov chain to determine the next token to generate.
* number-of-lines: Number (integer) of lines to generate.

## Usage:
* python markov.py type input chain-size number-of-lines

## Input constraints:
* Text must contain at least one newline character (i.e., '\n').

## Example:
Run the following in your terminal:
* python markov.py words file.txt 3 10
* python markov.py words ./data/ 4 50
* python markov.py chars ./data/Shakespeare-Works 3 50
* python markov.py chars ./data/ 5 50

## Explanation of Markov text generators:

A Markov text generator takes a piece of text as input and outputs new text
that is seemingly random. It may even make syntactical and/or semantic sense
if properly seeded with input text.

It accomplishes this by splitting the inputted text into tokens based on 
some separation character. This can result in individual characters or 
sequences of characters (recognized as words if the separation
character is a space).

It then creates a chain of these tokens based on the order of their appearance 
in the text. The length of this chain is chosen by the generator's user.
It then adds the token appearing immediately after this chain of tokens to a
list that is associated with that particular chain of tokens. Repeating this
process for all inputted text creates the Markov chain.

To generate the random text, the program chooses a chain
of tokens as the starting point of the output text.

It then chooses a random token from the list of tokens associated with the
chain and add that token to the output text.

After, it extends the chain of tokens to include this next token while
removing the first token from the chain. This creates a new chain of tokens
to then choose another random token from the list associated with the chain.

After some determined stopping point, the generator ceases to create more
text.

## Explanation Example

So, let's say I have the input text "I like bananas and apples and oranges."

Let's say I want to split this text by spaces, isolating the words and
character(s) that come immediately after the word.

I also want the chain's length (chain-size from 'Features' above) to be
1.

So the following chain would be created with its associated next tokens:

    chain of tokens: list of tokens coming after the chain in the text

    "I": ["like"]
    "like": ["bananas"]
    "bananas": ["and"]
    "and": ["apples", "oranges."]
    "apples": ["and"]

As you can see, the chain "and" has two different words it sees after it in
the sentence.

So, there's a 50% probability that "apples" or "oranges." will come after the
word "and" according to this sentence. However, with the other words there
is a 100% probability that the next word will be the only one contained
in their list.

You can imagine how more text and chains with lengths greater than 1 will
lead to more random and original sentences.

Suppose we don't have any separation. Doing this by character makes it more
interesting. It will generate more random words, some misspelled because
of the random aspects of chain, and will make less semantic sense
than creating chains via words (characters separated by a space).

## Notes about this particular implementation:

This particular implementation determines the point to stop generating
text by how many newlines it encounters while generating the text.

The user can specify whether to tokenize (separate) the input text by
words (characters separated by a space) or by individual characters.

For the next four paragraphs, I will be speaking as if the user wants
to tokenize the input text into individual words. Note that the same
behavior as described below can also be seen if the input text is tokenized
into individual characters.

The randomness of the output depends solely on the diversity of the input.
If the input is unique, then the output may be unique. For example,
if one gives the text generator a work of Shakespeare then that text
is likely to be unique on its own, so the output may seem extremely
similar the inputted text. However, if many similar sentences are inputted
then the output will seem very random.

If parameters are set properly, an infinite loop (i.e., the program runs forever)
can be encountered. This is caused by multiple repetitions of words in 
a row and setting the chain-size to a small number so the only words that
can follow the word is the word itself (caused by the repetitions).

Infinite loops can also be seen if no newlines can be reached from the
current chain of words.

Notice that as you increase the chain-size, the sensibility of the lines
increases, but also the familiarity of the lines increases. So you may
see that there are word-for-word excerpts of lines from text are outputted.
This is because not enough inputted text was given, so not enough variety
(choices of following words) exists.
