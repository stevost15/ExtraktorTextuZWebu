import os
import nltk
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from newspaper import Article

os.environ['NLTK_DATA'] = '/tmp/nltk_data'
nltk.download('punkt', download_dir='/tmp/nltk_data')
nltk.download('punkt_tab', download_dir='/tmp/nltk_data')

app = FastAPI(title="Extraktor článků API", description="Vrátí čistý text z webu")

class ArticleRequest(BaseModel):
    url: str

@app.post("/api/extract")
def extract_text(request: ArticleRequest):
    try:
        article = Article(request.url)
        
        article.download()
        
        article.parse()

        return {
            "status": "success",
            "data": {
                "title": article.title,
                "authors": article.authors,
                "publish_date": article.publish_date,
                "text": article.text
            }
        }
        
except Exception as e:
    raise HTTPException(status_code=400, detail=f"Něco se pokazilo: {str(e)}")