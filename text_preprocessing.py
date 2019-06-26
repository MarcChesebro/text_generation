import re
from util import load_file

def clean_tokenize_text(text, remove='[?!,.()[\]{}\'"]'):

    cleaned_text = text.replace('-', ' ')
    cleaned_text = re.sub(remove, '', cleaned_text)
    tokens = cleaned_text.split()

    tokens = [word.lower() for word in tokens if word != '' and word.isalpha()]

    return tokens

def sequence_tokens(tokens, sequence_length=50):
    length = sequence_length + 1
    sequences = []
    token_length = len(tokens)
    for i in range(length, token_length):
        sequence = tokens[i-length:i]

        sequences.append(' '.join(sequence))

    return sequences

def save_sequences(sequences, filename):
    data = '\n'.join(sequences)
    with open(filename, 'w') as file:
        file.write(data)


if __name__ == "__main__":
    filename = 'plato.txt'
    text = load_file(filename)
    save_sequences(sequence_tokens(clean_tokenize_text(text)), 'sequences.txt')
