from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
import os
from dotenv import load_dotenv
import json

# Ortam değişkenlerini yükle
load_dotenv()

# Google Gemini API anahtarını ayarla
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

app = FastAPI()

class KeywordRequest(BaseModel):
    keyword: str

@app.get("/")
def root():
    return {"message": "Hello, World!"}

@app.post("/generate-company-names")
async def generate_company_names(request: KeywordRequest):
    try:
        # Prompt'u oluştur
        prompt = (f"A new company will be established and this company will be a software company. "
                  f"I want to give a special name for this company, such as 'Google', 'Hyper', 'Tesla'. "
                  f"Let the name be at least 5 characters long. "
                  f"'{request.keyword}' should be used as the keyword. It doesn't need to be something meaningful, "
                  f"it must be a name that will become a brand. Therefore, there is no need for every word to start with a keyword, "
                  f"you can incorporate it into the words. Can you suggest me about 40 names like this? "
                  f"Can you please provide these suggestions in a single row without titles or other text?")

        # Modeli oluştur ve prompt ile istekte bulun
        model = genai.GenerativeModel('gemini-1.0-pro-latest')
        response = model.generate_content(prompt)

        # Yanıtı döndür
        company_names = {"company_names": response.text}

        # JSON verisini dosyaya kaydet
        with open("company_names.json", "w") as f:
            json.dump(company_names, f)

        return company_names

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/get-company-names")
async def get_company_names():
    try:
        # JSON verisini dosyadan oku
        with open("company_names.json", "r") as f:
            company_names = json.load(f)

        # JSON verisini döndür
        return company_names

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




# Uygulamayı çalıştırmak için aşağıdaki komutu kullanabilirsiniz
# 1. adım : uvicorn main:app --reload
# 2. adım yeni bir terminal: curl -X POST http://127.0.0.1:8000/generate-company-names -H "Content-Type: application/json" -d "{\"keyword\": \"example\"}"

#3. adım web: http://127.0.0.1:8000/get-company-names 


# sanal ortamı oluşturulduğunda ;  
# 1.adım :virtualenv venv
# 2.adım :pip install fastapi  
# 3.adım:pip install uvicorn
# 3.adım: pip install google-generativeai
#4.adım: uvicorn main:app --reload
# 5.adım: curl -X POST http://127.0.0.1:8000/generate-company-names -H "Content-Type: application/json" -d "{\"keyword\": \"example\"}"

#sanal ortamda kodu çalıştırmak için ;    Windosws : venv\Scripts\activate  "uvicorn main:app --reload"
#sanal ortamda kodu çalıştırmak için ;    Linux / Mac : source venv/bin/activate  "uvicorn main:app --reload"

# İşiniz bittiğinde sanal ortamı devre dışı bırakmak için 'deactivate' komutunu kullanabilirsiniz.