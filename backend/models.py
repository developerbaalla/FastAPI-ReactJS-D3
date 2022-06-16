# from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy import *
from sqlalchemy.orm import relationship

from db import Base


# Many to Many adds an association table between two classes Sentence & SentenceKeyword. 
sentence_keyword_association = Table(
    "association",
    Base.metadata,
    Column("sentences_id", ForeignKey("sentences.id")),
    Column("sentence_keywords_id", ForeignKey("sentence_keywords.id")),
)

# Main 'Sentence' model/table
class  Sentence(Base):
    __tablename__ = "sentences"

    # fields 
    id = Column(Integer,primary_key=True, autoincrement=True)
    date = Column(Date, nullable=True)
    sentence = Column(Text, nullable=True)
    sentence_sentiment_net = Column(Float, nullable=True)
    sentence_sent_score = Column(Float, nullable=True)
    sentence_sentiment_label = Column(Boolean, default=False)

    sentence_keywords = relationship("SentenceKeyword", secondary=sentence_keyword_association, back_populates="sentence")
    categories = relationship("Category", back_populates="sentence")
    sentence_shorts = relationship("SentenceShort", back_populates="sentence")
    sentence_sentiments = relationship("SentenceSentiment", back_populates="sentence")
    sentence_entities = relationship("SentenceEntity", back_populates="sentence")

class SentenceKeyword(Base):
    __tablename__ = "sentence_keywords"
    id = Column(Integer, primary_key=True, autoincrement=True)
    value = Column(String(255), nullable=True)
    # sentence_id = Column(Integer, ForeignKey("sentences.id"))
    sentence = relationship("Sentence", secondary=sentence_keyword_association, back_populates="sentence_keywords")

# A one to many relationship places a foreign key on the child table referencing the parent.
class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, autoincrement=True)
    value = Column(String(255), nullable=True)
    sentence_id = Column(Integer, ForeignKey("sentences.id"))
    sentence = relationship("Sentence", back_populates="categories")

class SentenceShort(Base):
    __tablename__ = "sentence_shorts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    value = Column(String(255), nullable=True)
    sentence_id = Column(Integer, ForeignKey("sentences.id"))
    sentence = relationship("Sentence", back_populates="sentence_shorts")

class SentenceSentiment(Base):
    __tablename__ = "sentence_sentiments"
    id = Column(Integer, primary_key=True, autoincrement=True)
    value = Column(String(255), nullable=True)
    sentence_id = Column(Integer, ForeignKey("sentences.id"))
    sentence = relationship("Sentence", back_populates="sentence_sentiments")

class SentenceEntity(Base):
    __tablename__ = "sentence_entities"
    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(String(255), nullable=True)
    value = Column(String(255), nullable=True)
    non = Column(Boolean, default=False)
    sentence_id = Column(Integer, ForeignKey("sentences.id"))
    sentence = relationship("Sentence", back_populates="sentence_entities")


# 'Young People' model/table
class  YoungPeople(Base):
    __tablename__ = "young_people"

    # fields 
    id = Column(Integer,primary_key=True, autoincrement=True)
    date = Column(Date, nullable=True)
    logits = Column(Float, nullable=True)
    net_sent = Column(Float, nullable=True)
    logits_mean = Column(Float, nullable=True)
    net_sent_mean = Column(Float, nullable=True)
    MA_logits = Column(Float, nullable=True)
    MA_net_sent = Column(Float, nullable=True)
    MA_net_sent_ema_alpha_0_1 = Column(Float, nullable=True)
    MA_net_sent_ema_alpha_0_3 = Column(Float, nullable=True)
    MA_net_sent_ema_alpha_0_5 = Column(Float, nullable=True)