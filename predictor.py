import numpy as np
import pandas as pd
import re
import nltk
import streamlit as st
import pickle
import joblib
from PIL import Image


image=Image.open('background.jpeg')
st.image(image, use_column_width=True)
st.title('Resturant Review Sentiment Analysis')
st.subheader('Single Review Classification')


#Data cleaning

def preprocess(str1):
    from nltk.corpus import stopwords
    from nltk.stem.porter import PorterStemmer
    ps = PorterStemmer()

    all_stopwords = stopwords.words('english')
    all_stopwords.remove('not')

    corpus=[]

    review = re.sub('[^a-zA-Z]', ' ', str1)
    review = review.lower()
    review = review.split()
    review = [ps.stem(word) for word in review if not word in set(all_stopwords)]
    review = ' '.join(review)
    corpus.append(review)

    # Loading BoW dictionary

    from sklearn.feature_extraction.text import CountVectorizer

    cvFile=r'analysis.pkl'
    cv = pickle.load(open(cvFile, "rb"))

    X_fresh = cv.transform(corpus).toarray()
    return X_fresh


#Predictions (via sentiment classifier)

def load_model():
    classifier = joblib.load(r'classifier model')
    return classifier

with st.spinner('Predicting...'):
    classifier=load_model()
y_pred=[]
st.subheader('Enter review:')
str1=st.text_area('', 'Type here')
if(str1!='Type here'):
    with st.spinner('Predicting...'):
        y_pred=classifier.predict(preprocess(str1))


if len(y_pred)!=0 and y_pred[0]=='1':
    st.success('The review is likely positive')
elif len(y_pred)!=0 and y_pred[0]=='0':
    st.error('The review is likely negative')
else:
    st.warning('Enter review to make predictions')