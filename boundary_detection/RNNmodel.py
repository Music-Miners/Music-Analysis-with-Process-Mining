import os
import numpy as np
import glob

from keras.layers import LSTM, Input, Dense, Activation, Embedding, Concatenate, Reshape
from keras.layers import RepeatVector, Permute
from keras.layers import Multiply, Lambda
import keras.backend as K 
from keras.models import Model
from keras.optimizers import RMSprop
from keras.utils import np_utils


def create_network(n_notes, n_durations, n_phrases, embed_size = 100, rnn_units = 256, use_attention = False):

    notes_in = Input(shape = (None,))
    durations_in = Input(shape = (None,))

    x1 = Embedding(n_notes, embed_size)(notes_in)
    x2 = Embedding(n_durations, embed_size)(durations_in)

    x = Concatenate()([x1,x2])

    x = LSTM(rnn_units, return_sequences=True)(x)

    if use_attention:

        x = LSTM(rnn_units, return_sequences=True)(x)

        e = Dense(1, activation='tanh')(x)
        e = Reshape([-1])(e)
        alpha = Activation('softmax')(e)

        alpha_repeated = Permute([2, 1])(RepeatVector(rnn_units)(alpha))

        c = Multiply()([x, alpha_repeated])
        c = Lambda(lambda xin: K.sum(xin, axis=1), output_shape=(rnn_units,))(c)
    
    else:
        c = LSTM(rnn_units)(x)
                                    
    phrases_out = Dense(n_phrases, activation = 'softmax', name = 'phrase')(c)
   
    model = Model([notes_in, durations_in], [phrases_out])
    

    if use_attention:
        att_model = Model([notes_in, durations_in], alpha)
    else:
        att_model = None


    opti = RMSprop(lr = 0.001)
    model.compile(loss=['binary_crossentropy', 'binary_crossentropy'], optimizer=opti)

    return model, att_model


def prepare_sequences(notes, durations, phrases, seq_len = 32):

    notes_input = []
    durations_input = []
    phrases_output = []

    for i in range(len(notes) - seq_len):
        notes_input.append(notes[i:i + seq_len])
        durations_input.append(durations[i:i + seq_len])

        phrases_output.append(phrases[i + seq_len])

    n_patterns = len(notes_input)

    notes_input = np.reshape(notes_input, (n_patterns, seq_len))
    durations_input = np.reshape(durations_input, (n_patterns, seq_len))
    network_input = [notes_input, durations_input]

    phrases_output = np_utils.to_categorical(phrases_output, num_classes=2)
    network_output = [phrases_output]

    return (network_input, network_output)