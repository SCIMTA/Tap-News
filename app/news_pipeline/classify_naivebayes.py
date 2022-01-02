import re
import gdown
import pickle
import joblib
import os
import scipy as sp
from sklearn.feature_extraction.text import TfidfTransformer, HashingVectorizer

def process(row):
    """
        row: a row of dataframe
        return: processed row
    """

    row = str(row)
    # lowercase content
    row = row.lower()

    # Convert url to URL
    row = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', 'URL', row)

    # Convert email to email
    row = re.sub(r'[\w\.-]+@[\w\.-]+', 'email', row)

    # Remove not alphameric
    row = re.sub(r'[^\w]', ' ', row)

    # Remove numbers
    row = ''.join([j for j in row if not j.isdigit()])

    # Remove emotion icons
    row = re.sub(
        ':\)|;\)|:-\)|\(-:|:-D|=D|:P|xD|X-p|\^\^|:-*|\^\.\^|\^\-\^|\^\_\^|\,-\)|\)-:|:\'\(|:\(|:-\(|:\S|T\.T|\.\_\.|:<|:-\S|:-<|\*\-\*|:O|=O|=\-O|O\.o|XO|O\_O|:-\@|=/|:/|X\-\(|>\.<|>=\(|D:',
        '', row)

    # Remove multiple marks
    row = re.sub(r"(\!)\1+", ' ', row)
    row = re.sub(r"(\?)\1+", ' ', row)
    row = re.sub(r"(\.)\1+", ' ', row)

    # Trim
    row = row.strip('\'"')
    row = row.strip()

    # remove addititonal white spaces
    row = re.sub('[\s]+', ' ', row)
    row = re.sub('[\n]+', ' ', row)

    return row


def download_model():
    try:
        # Download SVM model
        print("###Downloading model from ggdrive###")
        url_svm = "https://drive.google.com/uc?id=1riWxNbsxdAKuGj8YNXSOb7dje_-8xAWC"
        output_svm = "../models/news_classify.skl"
        gdown.download(url_svm, output_svm, quiet=False)

        url_tfidf = "https://drive.google.com/uc?id=1YDr3Wb35qwsIUS4BzV4fx5WCTO85UnyP"
        output_tfidf = "../models/tfidf.pickle"
        gdown.download(url_tfidf, output_tfidf, quiet=False)
        print("##Success!!")
    except Exception as err:
        print("Something happend...")
        print(err)


def load_model():
    """
        Load classify model

        return: classify_model, tfidf_model
    """
    if (os.path.isfile("./models/news_classify.skl")):
        try:
            # Assign model
            classify_model = joblib.load("./models/news_classify.skl")
            tfidf_model = pickle.load(open("./models/tfidf.pickle", "rb"))
        except Exception as err:
            print("Something happend, redownloading model...")
            # download_model()
            # Assign model
            classify_model = joblib.load("../models/news_classify.skl")
            tfidf_model = pickle.load(open("../models/tfidf.pickle", "rb"))

        print("Model loaded!!!!!!!!!")

    else:
        download_model()
        # Assign model
        classify_model = joblib.load("../models/news_classify.skl")
        tfidf_model = pickle.load(open("../models/tfidf.pickle", "rb"))
        print("Model loaded!!!!!!!!!")

    return classify_model, tfidf_model


def batdongsan_filter(content, classify_model, tfidf_model):
    hash_size = 5000
    hashed_vector = HashingVectorizer(n_features=hash_size, ngram_range=(1, 3)).fit_transform([content])
    tfidf_vector = tfidf_model.transform(hashed_vector)
    sparse_m = sp.sparse.bsr_matrix(tfidf_vector)
    res = classify_model.predict_proba(sparse_m.todense())
    print("Content: " , content[:30] , '... | ' , "score: " , res[0][2])
    return res[0][2]

