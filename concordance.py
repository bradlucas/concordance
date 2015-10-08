#!/usr/bin/python
"""Code Sample: V2

Please provide a code sample to answer the following question. The code can be in the language of your choice.

Given an arbitrary text document written in English, write a program that will generate a concordance, i.e. an alphabetical list of all word occurrences, labeled with word frequencies. Bonus: label each word with the sentence numbers in which each occurrence appeared.

Sample Result (using instructions as input)
-------------------------------------------

a	{2:1,1}
all	{1:1}
alphabetical 	{1:1}
an	{2:1,1}
appeared	{1:2}
arbitrary	{1:1}
bonus	{1:2}
concordance	{1:1}
document	{1:1}
each	{2:2,2}
english	{1:1}
frequencies	{1:1}
generate	{1:1}
given	{1:1}
i.e.	{1:1}
in	{2:1,2}
label	{1:2}
labeled	{1:1}
list	{1:1}
numbers	{1:2}
occurrence	{1:2}
occurrences	{1:1}
of	{1:1}
program	{1:1}
sentence	{1:2}
text	{1:1}
that	{1:1}
the	{1:2}
which	{1:2}
will	{1:1}
with	{2:1,2}
word	{3:1,1,2}
write	{1:1}
written	{1:1}


Notes
-----

Read the file from the command line
Lower case the contents so the results match 
Split the text into sentences
For each sentence split into words
Count the number of words and track which sentences contain each instance of each word
Print the results to match the sample output (see notes in report function)


"""
__author__ = "Brad Lucas"
__email__ = "bradleywlucas@gmail.com"
__date__ = "01/13/15"

def process_file(filename):
    """For a given filename read it's contents to a string and pass the string to the process function'"""
    return process(read_file_to_string(filename))


def read_file_to_string(filename):
    """Read the contents of filename and return as a string"""
    with open(filename, 'r') as in_file:
        text = in_file.read()
        return text


def split_to_sentences(text):
    """Split a text into sentences

    Some things to consider:
    - Sentences are delimited by a period, question mark or exclamation point
    - Simply spltting on period won't work because of abbreviations and words like i.e.
    - Carriage returns will confuse things so replace them with a space to ensure each sentence fits on one line
    """
    new_str = text.replace('\n', ' ')

    # this doesn't work because abbreviations and words like i.e. will cause sentence breaks
    # return new_str.split('.?!')

    # Using a regex 
    # @see http://stackoverflow.com/a/25736082
    import re

    return re.compile("(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s").split(new_str)


def split_to_words(sentence):
    """Return a list of words contained in the sentence

    - Some words have a trailing : or , which we'll remove before splitting
    - Also, the regex in split_to_sentences is leaving the trailing period in so we'll remove that as well
    """
    new_str = sentence.replace(':', '').replace(',', '')
    new_str = new_str.rstrip('.')
    return new_str.split(' ')


def process(text):
    """Process a text string and return a dictionary with unique words as the keys and values which contain the word count and list of sentence numbers
    
    - return diction with words as keys
    - the value is a tuple containing the word count and a list of sentence numbers
    """
    rtn = {}
    sentences = split_to_sentences(text.lower())
    sentence_count = 0
    for s in sentences:
        sentence_count += 1
        for w in split_to_words(s):
            if len(w) < 1: continue  # ignore empty words
            if w not in rtn:
                # add
                rtn[w] = 1, [sentence_count]
            else:
                # update
                cnt, l = rtn[w]
                cnt += 1
                l.append(sentence_count)
                rtn[w] = cnt, l
    return rtn


def report(dict):
    """Print the dictionary returned from the process routine

    - sort dictionary by key
    - print key name followed by {word_count: list_of_sentence_numbers }
    - for example,
    - word	{3:1,1,2}

    - to print a list without []s, map the str function of each int and join them with commas
    """
    for key in sorted(dict.iterkeys()):
        print "%s\t{%d:%s}" % (key, dict[key][0], ','.join(map(str, dict[key][1])))


test_string = """Given an arbitrary text document written in English,
write a program that will generate a concordance, i.e. an alphabetical
list of all word occurrences, labeled with word frequencies. Bonus:
label each word with the sentence numbers in which each occurrence
appeared."""

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] != "--pylab":
        report(process_file(sys.argv[1]))
    else:
        report(process(test_string))
