from numpy import array
from pickle import dump
from keras.preprocessing.text import Tokenizer
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Embedding

def load_file(filename):
    with open(filename, 'r') as file:
        text = file.read()
    return text

def get_sequences(filename='sequences.txt'):
    text = load_file(filename)
    return text.split('\n')

def create_model(sequence_length):
    model = Sequential()
    model.add(Embedding(vocab_size, 50, input_length=sequence_length))
    model.add(LSTM(100, return_sequences=True))
    model.add(LSTM(100))
    model.add(Dense(100, activation='relu'))
    model.add(Dense(vocab_size, activation='softmax'))

    return model

if __name__ == '__main__':
    tokenizer = Tokenizer()
    sequences = get_sequences()
    tokenizer.fit_on_texts(sequences)
    encoded_seq = tokenizer.texts_to_sequences(sequences)
    vocab_size = len(tokenizer.word_index) + 1

    encoded_seq = array(encoded_seq)
    prev_words = encoded_seq[:,:-1]
    next_word = encoded_seq[:,-1]

    # One hot encode next_word
    next_word = to_categorical(next_word, num_classes=vocab_size)

    sequence_length = prev_words.shape[1]

    model = create_model(sequence_length)

    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    model.fit(prev_words, next_word, batch_size=1, epochs=2)

    model.save('model.h5')

    dump(tokenizer, open('tokenizer.pkl', 'wb'))

