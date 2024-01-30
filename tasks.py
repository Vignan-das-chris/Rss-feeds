from celery import Celery
from .database import database
import time
import re
from logging_config import logging


from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.classify import NaiveBayesClassifier
from sklearn.feature_extraction.text import TfidfVectorizer



app = Celery('news_aggregator')

@app.task
def process_article(article_id):
    from sqlalchemy.orm import Session  

    session = Session() 

    try:
        article = session.query(Article).filter_by(id=article_id).first()
        text = article.content

       
        text = text.lower()
        text = re.sub(r'[^\w\s]', '', text)
        tokens = word_tokenize(text)
        tokens = [word for word in tokens if word not in stopwords.words('english')]
        stemmer = PorterStemmer()
        stemmed_tokens = [stemmer.stem(token) for token in tokens]
        cleaned_text = ' '.join(stemmed_tokens)

        
        model = None  
        vectorizer = TfidfVectorizer()
        features = vectorizer.fit_transform([cleaned_text])
        predicted_category = model.predict(features)[0]

        
        article.category = predicted_category
        session.commit()

        print(f"Article {article_id} processed and categorized as {predicted_category}")
    except Exception as e:
        
        logging.error(f"Error processing article {article_id}: {e}")
        session.rollback()  

    finally:
        session.close() 

def run_task():
    logging.info("Starting task execution")
    # ... perform task logic ...
    logging.debug("Task completed successfully")
        

