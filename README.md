# sks-raster
Skogsstyrelsens öppna rasterdata

## Innehållsförteckning
- [Syfte](#syfte)
- [Tillgängliga data](#tillgängligt-data)
- [ESRI Image server REST API](#esri-image-server-rest-api)
- [Åtkomst och inloggning](#åtkomst-och-inloggning)
- [Exempelkod](#exempelkod)
- [Friskrivning](#friskrivning)
- [Licens](#licens)

## Syfte
Skogsstyrelsen erbjuder script och exempelkod för utvecklare som vill använda sig av myndighetens öppna rasterdata för utveckling av sina egna produkter eller tillämpningar. Avsikten är att underlätta nedladdning av råa data, eller data som är ett resultat av en on-the-fly-analys. Dessa data hämtas från Skogsstyrelsens externa bildserver som är byggd på en [ESRI ArcGIS Image Server](https://enterprise.arcgis.com/en/image/latest/get-started/windows/what-is-arcgis-image-server-.htm). Scripten som erbjuds visar exempel på hur anropen kan se ut och hur dessa kan systematiseras för att bli effektiva.
Var noga med att läsa igenom Skogsstyrelsens [Friskrivning](#friskrivning) nedan. I tillägg till friskrivningen vill vi att användare noterar att snabba svarstider på varje anrop inte kan garanteras. De kan beroende på belastning och komplexitet variera mycket.


## Tillgängligt data
Skogsstyrelsens öppna tjänster listas under https://www.skogsstyrelsen.se/sjalvservice/karttjanster/geodatatjanster/rest/

För att klicka sig vidare komma åt information om respektive dataset krävs inloggningsuppgifter, se [Åtkomst och inloggning](#åtkomst-och-inloggning)

## ESRI Image server REST API
Skogsstyrelsen använder sig av ESRIs plattform för geodata. Se [ESRI:s egen REST API-dokumentation](https://developers.arcgis.com/rest/services-reference/enterprise/image-service.htm) för en djupare och mer detaljerad förståelse om hur bildtjänsterna fungerar, vilka anrop som kan göras och hur anropen byggs upp.

## Åtkomst och inloggning
Du behöver ett användarkonto för att kunna ladda ner eller använda Skogsstyrelsens rasterdata i egna system. Kontot använder du varje gång du laddar ner data eller kopplar upp dig mot en tjänst.

Skogsstyrelsen ser gärna att ett användarkonto används per företag/organisation som sedan kan spridas vidare internt. Detta gäller inte privatpersoner.

Navigera till [Beställa användarkonto för Skogsstyrelsens rasterdata](https://www.skogsstyrelsen.se/sjalvservice/karttjanster/geodatatjanster/skaffa-anvandarkonto/) och fyll i formuläret för att ansöka om ett konto.

När kontot har erhållits, är det dessa uppgifter som ska användas för samtliga anrop mot REST-tjänsterna, så som visas i [exempelkoden](./examples).

## Exempelkod
I mappen [examples](./examples) finns python kod som visar hur man kan koppla upp sig mot bildtjänsterna för att hämta ut data från Skogsstyrelsens bildtjänster. Detta är en teknisk beskrivning av hur man kan hämta och kombinera data till en lämplig samansättning för till exempel visning eller AI-tillämpningar.


## Friskrivning
Skogsstyrelsen friskriver sig från eventuella felaktigheter i kod.
Skogsstyrelsen friskriver sig från ansvar för fel, förseningar, avbrott eller 
andra fel eller störningar som kan uppstå i den tekniska driften och därmed i 
tillgången till Geodataprodukterna. Skogsstyrelsen tar inte heller något ansvar för fel som 
kan uppstå på grund av den teknik eller de programvaror som användaren 
använder för att få åtkomst till Geodataprodukterna. Skogsstyrelsen friskriver 
sig också från ansvar för skada eller annan olägenhet som kan uppkomma 
till följd av användandet av Geodataprodukterna för sig eller tillsammans 
med annan information. Skogsstyrelsen friskriver sig från ansvar för fel eller 
förändringar i Geodataprodukterna sedan de levererats/distribuerats från 
Skogsstyrelsen till användaren alternativt när informationen kommit ur 
Skogsstyrelsens kontroll.

## Licens
Se [LICENSE](./LICENSE) samt [villkor för nyttjande av Skogsstyrelsen öppna geodata](https://www.skogsstyrelsen.se/sjalvservice/karttjanster/geodatatjanster/villkor-for-nyttjande-av-skogsstyrelsens-kartdatabaser/)
