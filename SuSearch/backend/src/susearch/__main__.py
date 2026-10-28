import webview
from models.document_chunker import DocumentChunker
from services.keyword_extractor import KeywordExtractor

class DataExtractor:
    """
    
    """
    def __init__(self, raw_document: str):
        self._chunker = DocumentChunker(raw_document)
        
        self.chunks = self._chunker.chunk_document()
        
        self._embedding_service = None
        self._keyword_service = None

    def get_chunks(self) -> list[str]:
        return self.chunks
    
class DesktopBridge:
    """ 
    Acts as a bridge between frontend and backend.
    """
    def __init__(self, data_extractor: DataExtractor):
        self._data_extractor = data_extractor
        self._window = None 
    
    def execute_search(self, query: str):
        return self._data_extractor.search(query)

document = """Kriterier för Region Skånes stöd till Miljö-
och Naturvårdsföreningar

1 Syfte med bidraget
Region Skåne samarbetar med och stödjer den idéburna sektorn för
att skapa ett långsiktigt hållbart Skåne och möta komplexa
samhällsutmaningar som Skåne står inför. Bidraget utgår från
hållbarhetsperspektivet med fokus på miljö- och klimat i den
regionala utvecklingsstrategin och syftar till att skapa ökade
möjligheter för idéburna organisationer att ta en aktiv roll i Skånes
miljöarbete.
Bidraget syftar till att skapa förutsättningar för organisationens
ordinarie verksamhet.

2 Vem kan söka?
Bidrag ges till idéburna organisationer, vars huvudsakliga syfte är att
bedriva naturvård, kulturmiljövård eller andra typer av miljö- och
klimatarbete. Organisationerna ska ha en tydlig regional prägel, där
verksamheten företrädesvis ska beröra hela Skåne. Verksamhet ska
kunna vara generaliserbar och tillämpbar i större delen av Skåne.

3 Övergripande kriterier
Föreningens verksamhet ska bidra till det strategiska området ”Hela
Skåne”, i den regionala utvecklingsstrategin ”Det Öppna Skåne 2030”.
vilket handlar om att det ska vara möjligt att bo, verka och leva i hela

3 (6)

DokumentID Ange dokumentID

Original lagras elektroniskt. Användaren ansvarar för att gällande version används.
Skåne. De frågor inom ”Hela Skåne” som är mest relevanta för detta
bidrag är tillgången till rekreation och friluftsliv samt behovet av en
ökad regional energiproduktion. Föreningens verksamhet ska därför
adressera minst en av dessa frågor. När det gäller rekreation och

friluftsliv ska föreningens verksamhet värna om det skånska natur-
och kulturlandskapet och därigenom skapa förutsättningar för att

bibehålla möjligheten till rekreation och friluftsliv i Skåne.
Föreningens verksamhet ska även bidra till de tvärgående
perspektiven ”Miljömässig, social och ekonomisk hållbarhet” samt
”Beredskap och resiliens” i den regionala utvecklingsstrategin ”Det
Öppna Skåne”. Inom hållbarhetsperspektivet ska föreningen
fokusera på det miljömässiga perspektivet. Det innebär att
föreningens verksamhet ska främja ekosystem, ekosystemtjänster
och biologisk mångfald, motverka klimatförändringar samt värna om
Skånes kultur- och naturlandskap. När det gäller beredskap och
resiliens innebär det för föreningens verksamhet framför allt att
bidra till den skånska natur- och kulturmiljöns förmåga att hantera
klimatförändringar samt att bidra till att skapa ett
energiförsörjningssystem med hög krisberedskap.

https://www.skane.se/regional-utveckling/regional-
utvecklingsstrategi/

4 Ska-krav
Föreningens verksamhet ska:
1. Vara huvudsakligen inriktad på antingen naturvård,
kulturmiljövård eller andra typer av miljö- och klimatarbete.
2. Bidra till det strategiska området ”Hela Skåne” samt de
tvärgående perspektiven ”Miljömässig, social och ekonomisk
hållbarhet” och ”Beredskap och resiliens” i den regionala
utvecklingsstrategin ”Det Öppna Skåne”.
3. Vara generaliserbar och tillämpbar i större delen av Skåne.

4 (6)

DokumentID Ange dokumentID

Original lagras elektroniskt. Användaren ansvarar för att gällande version används.
4. Vara öppen för medlemmar från hela Skåne.
5. Innefatta informationsspridning om föreningens verksamhet
till andra än de egna medlemmarna, genom att arrangera eller
delta i minst en (1) fysisk aktivitet per år med fokus på
informationsspridning.
6. Följa regionala utvecklingsnämndens riktlinjer för idéburna
organisationer.

https://utveckling.skane.se/siteassets/publikationer/riktlinjer-
bidrag-riktat-mot-ideburen-sektor.pdf

5 Bedömningsgrunder
Detta bidrag är ett av Region Skånes verksamhetsbidrag till idéburen
sektor. Alla ansökningar som uppfyller ska-kraven enligt ovan
beviljas medel men beloppet kan reduceras om budgeterade medel
från Region Skåne inte täcker summan av ansökningarna. Region
Skåne förbehåller sig rätten att bedöma ansökan utifrån kriterierna
beskrivna i detta dokument. De ansökningar som uppfyller samtliga
ska-krav utvärderas utifrån en modell. En kvalitativ bedömning görs
utifrån hur väl verksamheten uppnår ska-kraven (1=bra, 2=mycket
bra, 3=utmärkt). Resultatet vägs in i bedömningen av hur medlen ska
fördelas mellan kvalificerade föreningar.

6 Utlysning
Bidraget utlyses på Region Skånes hemsida. Utlysningstiden är
normalt 1 mars - 2 maj.

https://utveckling.skane.se/soka-stod/bidrag-att-soka/miljo--och-
naturvardsforeningar/

5 (6)

DokumentID Ange dokumentID

Original lagras elektroniskt. Användaren ansvarar för att gällande version används.
7 Ansökan
Föreningen ska efter att tagit del av riktlinjer och kriterier inkomma
med sin ansökan till Region Skåne, senast det datum som annonseras
på hemsidan. En ansökan består av ett ifyllt ansökningsformulär som
finns att ladda ner på hemsidan, samt ett antal bilagor. Formuläret
ska vara fullständigt ifyllt och undertecknat och samtliga bilagor ska
finnas med när ansökan skickas in till Region Skåne.
Ansökan skickas via e-post till miljoforeningsbidrag@skane.se
Det ges en (1) möjlighet till att göra kompletteringar. Dessa måste
inkomma senast två veckor från att den ansökande kontaktats av
Region Skåne i ärendet. Handlingar som inkommer efter det kommer
inte att behandlas.

7.1 Bilagor ansökan
Till ansökan ska bifogas:
1. Aktuella stadgar, om det är första gången föreningen söker
eller om förändringar gjorts sedan stadgarna senast skickades
in.
2. Verksamhetsplan och budget för innevarande år.
3. Förteckning över styrelsens ledamöter samt antal medlemmar.
4. Av styrelsen undertecknad årsredovisning från senast
upprättade år, eller årsbokslut alternativt förenklat bokslut
(Bokföringslag, 1999:1078 och Bokföringsnämndens
rekommendationer). Till årsredovisningen ska bifogas:
• Revisionsberättelse som beskriver ansvarsfrihet för
styrelsen och som är undertecknad av revisor.
• Verksamhetsberättelse som har antagits vid årsmötet.
• Årsmötesprotokoll som är undertecknat av ordförande
samt justerat.

6 (6)

DokumentID Ange dokumentID

Original lagras elektroniskt. Användaren ansvarar för att gällande version används.
8 Beslut
Beslut om stöd till miljö- och naturvårdsföreningar tas av regionala
utvecklingsnämnden, genom delegation. Avdelningen för regional
utveckling bereder ärendet. Godkända ansökningar betalas ut efter
att beslutet vunnit laga kraft.

9 Miljökriterier vid beviljande av bidrag
Idéburna organisationer som med sin verksamhet, helt eller delvis,
finansieras av Region Skåne ska ta ansvar för sin miljöpåverkan och
bidra till att Region Skånes miljöpolicy och miljömål uppnås.
Verksamheter som får bidrag på minst tio prisbasbelopp per år
omfattas av särskilda krav som bidrar till Region Skånes miljöarbete,
enligt Region Skånes Miljöbevis. De verksamheter som får under tio
prisbasbelopp per år (2025: 588 000 kr) i finansiering ska genom sitt
miljöarbete bidra till Region Skåne miljöpolicy och miljöprogram,
men behöver inte beskriva eller rapportera det till Region Skåne.
"""


if __name__ == '__main__':
    data_extractor = DataExtractor(document)
    chunks = data_extractor.get_chunks()

    keyword_extractor = KeywordExtractor()
    yake_results = keyword_extractor.get_yake(chunks)
    ner_results = keyword_extractor.get_ner(chunks)

    print(f"\nAmount of chunks: {len(chunks)}")
    
    for index, (chunk, keywords, ner) in enumerate(zip(chunks, yake_results, ner_results), start=1):

        print(f"Chunk {index} YAKE words")
        for item in keywords:
            print(f"   {item['keyword']} (score: {item['score']})")

        print(" ")
        print(f"Chunk {index} NER words")
        for ent in ner:
                print(f"   {ent['word']} ({ent['entity_group']}, score: {ent['score']})")

        print("\n" + " " * 20  + "\n")


    # bridge = DesktopBridge(data_extractor)


    # window = webview.create_window(
    #     title="SuSearch",
    #     url="http://localhost:5173",
    #     js_api=bridge
    # )

    # def on_closing():
    #         print("Closing start cleanup.")
    #         data_extractor.cleanup()

    # window.events.closing += on_closing

    # webview.start(debug=True)
