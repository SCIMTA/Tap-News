import re
import gdown
import os

import numpy as np

import tensorflow as tf
import transformers #huggingface transformers library
from transformers import AutoModel, AutoTokenizer
from underthesea import word_tokenize

from sklearn.preprocessing import LabelEncoder
import sklearn

import six

def process(text):
  text = str(text)
  text = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', 'URL', text)
  text = re.sub('@[^\s]+', 'AT_ABC', text)
  text = re.sub(r'\n', ' ', text)
  text = re.sub(r'([\w]+\) )', '.', text)
  text = re.sub(r'([\d]+\. )', '', text)
  text = re.sub(r'[^aAàÀảẢãÃáÁạẠăĂằẰẳẲẵẴắẮặẶâÂầẦẩẨẫẪấẤậẬbBcCdDđĐeEèÈẻẺẽẼéÉẹẸêÊềỀểỂễỄếẾệỆfFgGhHiIìÌỉỈĩĨíÍịỊjJkKlLmMnNoOòÒỏỎõÕóÓọỌôÔồỒổỔỗỖốỐộỘơƠờỜởỞỡỠớỚợỢpPqQrRsStTuUùÙủỦũŨúÚụỤưƯừỪửỬữỮứỨựỰvVwWxXyYỳỲỷỶỹỸýÝỵỴzZ0-9., ]', '', text)
#   text = text.replace('.', '. ')
#   text = text.replace(' .', '. ')
  text = re.sub(r'[\s]+', ' ', text)
  text = text.strip('.')
  text = text.strip('\'"')
  text = text.strip()
  text = text.lower()
  return text


def download_model():
    try:
        # Download SVM model
        print("###Downloading model from ggdrive###")
        url_svm = "https://drive.google.com/uc?id=1m8y79sTEIjMGIJ5R3fFKNf4yITKHheam"
        output_svm = "../models/model.hdf5"
        gdown.download(url_svm, output_svm, quiet=False)

        print("##Success!!")
    except Exception as err:
        print("Something happend...")
        print(err)


def build_model(transformer, loss='categorical_crossentropy', max_len=512):
    input_word_ids = tf.keras.layers.Input(shape=(max_len,), dtype=tf.int32, name="input_word_ids")
    sequence_output = transformer(input_word_ids)[0]
    cls_token = sequence_output[:, 0, :]
    # adding dropout layer
    x = tf.keras.layers.Dropout(0.3)(cls_token)
    # using a dense layer of 13 neurons as the number of unique categories is 40.
    # out = tf.keras.layers.Dense(27, activation='softmax')(x)
    out1 = tf.keras.layers.Dense(784, activation='relu')(x)
    out2 = tf.keras.layers.Dropout(0.1)(out1)
    out3 = tf.keras.layers.Dense(392, activation='relu')(out2)
    out4 = tf.keras.layers.Dropout(0.1)(out3)
    out5 = tf.keras.layers.Dense(196, activation='relu')(out4)
    out6 = tf.keras.layers.Dropout(0.1)(out5)
    out7 = tf.keras.layers.Dense(98, activation='relu')(out6)
    # out8 = tf.keras.layers.Dropout(0.1)(out7)
    out9 = tf.keras.layers.Dense(27, activation='softmax')(out7)
    model = tf.keras.Model(inputs=input_word_ids, outputs=out9)
    # using categorical crossentropy as the loss as it is a multi-class classification problem
    # resign loss
    lossF = tf.keras.losses.CategoricalCrossentropy(from_logits=True)

    model.compile(tf.keras.optimizers.Adam(lr=3e-5, beta_1=0.9, beta_2=0.999), loss=lossF, metrics=['accuracy'])
    return model

def load_model():
    """
        Load classify model

        return: model, encoder
    """
    # print("PAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA: ", os.getcwd())
    if (os.path.isfile("./models/model.hdf5")):
        try:
            # Assign model
            tokenizer = AutoTokenizer.from_pretrained("Geotrend/bert-base-vi-cased")
            transformer_layer = transformers.TFAutoModel.from_pretrained('Geotrend/bert-base-vi-cased')
            model = build_model(transformer_layer, max_len=512)
            model.summary()
            model.load_weights(
                './models/model.hdf5')

            # Assign label
            encoder = LabelEncoder()
            encoder.classes_ = np.load('./models/classes.npy', allow_pickle=True)
        except Exception as err:
            print("Something happend, redownloading model...")
            # download_model()
            # Assign model
            tokenizer = AutoTokenizer.from_pretrained("Geotrend/bert-base-vi-cased")
            transformer_layer = transformers.TFAutoModel.from_pretrained('Geotrend/bert-base-vi-cased')
            model = build_model(transformer_layer, max_len=512)
            model.summary()
            model.load_weights(
                './models/model.hdf5')

            # Assign label
            encoder = LabelEncoder()
            encoder.classes_ = np.load('./models/classes.npy', allow_pickle=True)

        print("Model loaded!!!!!!!!!")

    else:
        download_model()
        # Assign model
        transformer_layer = transformers.TFAutoModel.from_pretrained('Geotrend/bert-base-vi-cased')
        model = build_model(transformer_layer, max_len=512)
        model.summary()
        model.load_weights(
            './models/model.hdf5')

        # Assign label
        encoder = LabelEncoder()
        encoder.classes_ = np.load('./models/classes.npy', allow_pickle=True)
        print("Model loaded!!!!!!!!!")

    return model, encoder.classes_, tokenizer


def word_seg_dash(text):
    return word_tokenize(text, format='text')


def regular_encode(texts, tokenizer, maxlen=512):
    # word tokenize before input to bert
    texts = list(map(word_seg_dash, texts))
    # encode
    enc_di = tokenizer.batch_encode_plus(
        texts,
        return_token_type_ids=False,
        pad_to_max_length=True,
        max_length=maxlen,
    )

    return np.array(enc_di['input_ids'])


def chungkhoan_filter_bert(content, classify_model_bert, encoded_classes, tokenizer):
    # t_start = time()
    BATCH_SIZE = 64
    # Encode input
    Xtest_encoded = regular_encode([content], tokenizer, maxlen=512)
    test_dataset = (
        tf.data.Dataset
            .from_tensor_slices(Xtest_encoded)
            .batch(BATCH_SIZE)
    )

    # making predictions
    preds = classify_model_bert.predict(test_dataset)       # add verbose=1 if you need more info
    # converting the one hot vector output to a linear numpy array.
    pred_classes = np.argmax(preds, axis=1)
    score = preds[0][pred_classes[0]]
    # extracting the classes from the label encoder
    # encoded_classes = encoder.classes_
    # mapping the encoded output to actual categories
    predicted_category = [encoded_classes[x] for x in pred_classes]

    # print("[ANNOUNCE] Predicted success after {} seconds".format(time()-t_start))
    return predicted_category[0], score
