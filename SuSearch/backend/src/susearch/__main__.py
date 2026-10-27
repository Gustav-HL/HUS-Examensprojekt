import torch
import torch.nn.functional as F
from transformers import AutoModelForTokenClassification, AutoTokenizer, AutoModel, pipeline
import webview
import gc

def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output[0]
    input_mask_expanded = (
        attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    )
    return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(
        input_mask_expanded.sum(1), min=1e-9
    )

class DataExtractor:
    def __init__(self, corpus):
        print("Loading Model")
        self.corpus = corpus
        self.tokenizer = AutoTokenizer.from_pretrained("KBLab/sentence-bert-swedish-cased")
        self.model = AutoModel.from_pretrained("KBLab/sentence-bert-swedish-cased")
        
        self.ner_tokenizer = AutoTokenizer.from_pretrained("KBLab/bert-base-swedish-cased-ner")
        self.ner_model = AutoModelForTokenClassification.from_pretrained(
            "KBLab/bert-base-swedish-cased-ner"
        )
        self.ner = pipeline(
            "ner",
            model=self.ner_model,
            tokenizer=self.ner_tokenizer,
            # Combines part words to whole words
            aggregation_strategy="simple",  
        )

        encoded = self.tokenizer(self.corpus, padding=True, truncation=True, return_tensors="pt")
        with torch.no_grad():
            output = self.model(**encoded)
        embeddings = mean_pooling(output, encoded["attention_mask"])
        self.corpus_embeddings = F.normalize(embeddings, p=2, dim=1)
        print("Done Loading")

    def search(self, query: str):
        if not query or not query.strip():
            return []

        encoded_query = self.tokenizer([query], padding=True, truncation=True, return_tensors="pt")
        with torch.no_grad():
            output = self.model(**encoded_query)

        query_emb = mean_pooling(output, encoded_query["attention_mask"])
        query_emb = F.normalize(query_emb, p=2, dim=1)[0]

        # self.ner_results = self.ner(corpus)

        scores = torch.mv(self.corpus_embeddings, query_emb)
        ranked = sorted(zip(self.corpus, scores.tolist()), key=lambda x: x[1], reverse=True)

        return [{"text": text, "score": round(score, 4)} for text, score in ranked]

    def cleanup(self):
        print("Closing Model")
        if hasattr(self, 'model'):
            del self.model
        if hasattr(self, 'tokenizer'):
            del self.tokenizer
        if hasattr(self, 'corpus_embeddings'):
            del self.corpus_embeddings
            
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        print("Cleared")


class DesktopBridge:
    def __init__(self, data_extractor: DataExtractor):
        self._data_extractor = data_extractor
        self._window = None 
    
    def execute_search(self, query: str):
        return self._data_extractor.search(query)

# List of test data
corpus = [
    # Tema: Hållbarhet & Energi
    "Vi behöver minska våra koldioxidutsläpp för att bromsa klimatförändringarna.",
    "Solceller och vindkraft är viktiga delar i övergången till förnybar energi.",
    "Fastigheten är certifierad enligt miljöbyggnad guld och sparar mycket energi.",
    "Sopsortering och återvinning av plast minskar belastningen på naturen.",
    "Fan! Vilket jävla skit. Sade Jesus år 12 efter kristus när han slog stortån på en list.",
    # Tema: IT, Kod & Databaser
    "Databasen har indexerats om för att snabba upp söktiderna i backend-systemet.",
    "Ett nytt REST API har implementerats med FastAPI och Pydantic.",
    "Utvecklingsteamet åtgärdade flera kritiska buggar inför fredagens produktionssättning.",
    "Versionshantering med Git gör det enklare att samarbeta i stora projekt.",
    "Bästa Leauge champions: Nunu, Kindred och såklart Mästarn",
    "HUT-produkten gör framsteg",
    # Tema: Matlagning & Bakning
    "Surdegsbrödet fick jäsa långsamt i kylskåpet över natten.",
    "Till såsen används schalottenlök, vitt vin och en klick smör.",
    "Rätten kryddas rikligt med färsk koriander, ingefära och chili.",
    "Pastan kokas tills den är al dente och vänds sedan i olivolja.",
    "Ge mig en påse chips.",
    "Snälla Kalle ge mig en påse chips! Jag svälter.",
    # Tema: Vardag, Resor & Vinter
    "Tåget mot Stockholm blev inställt på grund av en signalstörning.",
    "Idag är det fredagen den 16e October 2026",
    "Under vintern fryser sjöarna till is och folk åker långfärdsskridskor.",
    "Katten sover på mattan framför den öppna spisen.",
    "Jag glömde mitt paraply hemma och blev genomblöt på väg till jobbet.",
    "Glen reste till Danmark med sin kompis Sven Svensson den förste av sitt namn",
]

if __name__ == '__main__':
    data_extractor = DataExtractor(corpus)
    bridge = DesktopBridge(data_extractor)

    window = webview.create_window(
        title="SuSearch",
        url="http://localhost:5173",
        js_api=bridge
    )

    def on_closing():
            print("Closing start cleanup.")
            data_extractor.cleanup()

    window.events.closing += on_closing

    webview.start(debug=True)