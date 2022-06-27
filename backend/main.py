from fastapi import FastAPI, HTTPException
import models
from db import engine
from sqlalchemy.orm import Session, joinedload
from fastapi.middleware.cors import CORSMiddleware

#create the database tables on app startup or reload
models.Base.metadata.create_all(bind=engine)

#initailize FastApi instance
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#sentence_keywords endpoint
#return the sentence tabel and associated keywords
@app.get("/sentence_keywords")
def sentence_keywords_list(keyword: str = '', limit: int = 10):
    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    try:
        # get sentence_keywords items
        if keyword != '':
            sentence_keywords = session.query(models.Sentence).filter(models.Sentence.sentence.ilike(f'%{keyword}%')).options(joinedload(models.Sentence.sentence_keywords)).order_by(models.Sentence.date.desc()).limit(limit).all()
        else:
            sentence_keywords = session.query(models.Sentence).options(joinedload(models.Sentence.sentence_keywords)).order_by(models.Sentence.date.desc()).limit(limit).all()

    except Exception as ex:
        raise HTTPException(status_code=404, detail=str(ex))

    finally:
        # close the session
        session.close()

    return sentence_keywords


#young_people endpoint
#return the the logits and some other information
@app.get("/young_people")
def young_people_list():
    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    try:
        # get all young_people items
        young_people_list = session.query(models.YoungPeople).with_entities(models.YoungPeople.id, models.YoungPeople.date, models.YoungPeople.logits, models.YoungPeople.net_sent, models.YoungPeople.logits_mean).order_by(models.YoungPeople.date.asc()).all()

    except Exception as ex:
        raise HTTPException(status_code=404, detail=str(ex))

    finally:
        # close the session
        session.close()

    return young_people_list