import keras
from keras import *
from keras import layers, optimizers
from keras.layers import Embedding, Conv1D, GlobalMaxPooling1D, Dense, Dropout
from keras.models import Model, model_from_json
from keras.preprocessing import *
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras import backend as K
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pickle
import pandas as pd
import numpy as np


def trainingcnn():

    keras.backend.clear_session()
    sms_df = pd.read_csv('D:\\feedbacksm\\feedbacksystem\\feedbacksystem\\static\\newdataset.csv')

    sms_df['Emotion'] = sms_df['Emotion'].replace("neutral", 1)
    sms_df['Emotion'] = sms_df['Emotion'].replace("negative",1)
    sms_df['Emotion'] = sms_df['Emotion'].replace("positive",2)

    labels = sms_df.values[:, 0]
    msgs = sms_df.values[:, 1]

    print(labels)

    print(msgs)

    train_texts, test_texts, train_labels, test_labels = train_test_split(msgs, labels, test_size=0.1, random_state=500)

    VOCABULARY_SIZE = 5000
    tokenizer = Tokenizer(num_words=VOCABULARY_SIZE)
    tokenizer.fit_on_texts(train_texts)

    print("Vocabulary created")

    meanLength = np.mean([len(item.split(" ")) for item in train_texts])
    #MAX_SENTENCE_LENGTH = int(meanLength + 5)
    MAX_SENTENCE_LENGTH=100
    print("MAX_SENTENCE LENGTH=",MAX_SENTENCE_LENGTH)
    trainFeatures = tokenizer.texts_to_sequences(train_texts)
    trainFeatures = pad_sequences(trainFeatures, MAX_SENTENCE_LENGTH, padding='post')
    # trainLabels = train_labels.values

    testFeatures = tokenizer.texts_to_sequences(test_texts)
    testFeatures = pad_sequences(testFeatures, MAX_SENTENCE_LENGTH, padding='post')
    # testLabels = test_labels.values

    print("Tokenizing completed")

    FILTERS_SIZE = 16
    KERNEL_SIZE = 5

    EMBEDDINGS_DIM = 10
    LEARNING_RATE = 0.001
    BATCH_SIZE = 32
    EPOCHS = 20

    print("embed=",EMBEDDINGS_DIM)
    print(len(trainFeatures[0]))

    maxlen=0

    for i in trainFeatures:
        if len(i)>maxlen:
            maxlen=len(i)
    print("maxlen=",maxlen)




    model = Sequential()
    model.add(Embedding(input_dim=VOCABULARY_SIZE + 1, output_dim=EMBEDDINGS_DIM, input_length=maxlen))
    model.add(Conv1D(FILTERS_SIZE, KERNEL_SIZE, activation='relu'))
    model.add(Dropout(0.5))
    model.add(GlobalMaxPooling1D())
    model.add(Dropout(0.5))
    model.add(Dense(8, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))

    optimizer = optimizers.Adam(lr=LEARNING_RATE)
    model.compile(optimizer=optimizer, loss='binary_crossentropy', metrics=['accuracy'])

    print(model.summary())

    history = model.fit(trainFeatures, train_labels, batch_size=BATCH_SIZE, epochs=EPOCHS)

    with open('tokenizer.pickle', 'wb') as handle:
        pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)
    model_json = model.to_json()
    with open("model.json", "w") as json_file:
        json_file.write(model_json)
    model.save_weights("model.h5")




trainingcnn()