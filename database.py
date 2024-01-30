from sqlalchemy import create_engine, or_
from sqlalchemy.orm import sessionmaker
from models import Base, Article
from logging_config import logging


engine = create_engine('postgresql://user:14748@localhost:5432/postgres')

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

def add_article(article_data):
    with Session() as session:
        existing_article = session.query(Article).filter(
            or_(
                Article.title == article_data['title'],  
                Article.url == article_data['url'] 
            )
        ).first()

        if not existing_article:
            article = Article(**article_data)
            session.add(article)
            session.commit()
        else:
            print(f"Article with title '{article_data['title']}' already exists (URL: {existing_article.url})")


def connect_to_database():
    try:
        db = connect_to_db()  # Assuming a function to connect to the database
        return db
    except DatabaseError as e:
        logging.error("Database connection error: %s", e)
        raise  # Re-raise the exception to propagate it

