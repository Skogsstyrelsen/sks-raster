# Exempelkod
## Förkrav
I samtliga exempel används python version 3, samt ett antal python paket som måste installeras innan koden kan köras. Dessa paket listas i dokumentationen i respektive exempel.

## Autentisering
Samtliga HTTP-anrop mot Skogsstyrelsens bildtjänster kräver autentisering. Metoden som används är så kallad 'Basic Authentication' vilket innebär att användarnamn och lösenord skickas med i headern i Base64 kodning. [Läs mer Basic Authentication här](https://developer.mozilla.org/en-US/docs/Web/HTTP/Authentication#basic_authentication_scheme). 

### Autentisering i exempelkoden
I exempelkoden används python och [requests](https://requests.readthedocs.io/en/latest/) paketet för att göra anrop mot bildservern. Detta paket har inbyggd funktionalitet för Basic Authentication:

```
response = requests.get("https://bildservern.se", auth=(USERNAME, PASSWORD))
```

Där USERNAME och PASSWORD är det användarnamn och lösenord (i klartext) för det konto som du fått av Skogsstyrelsen för access till bildservrarna. I samtliga anrop krävs det att man använder HTTPS. [Klicka här för att se hur du beställer ett konto för access](https://www.skogsstyrelsen.se/sjalvservice/karttjanster/geodatatjanster/skaffa-anvandarkonto/). 

Andra python paket kan ha andra implementationer för Basic Authentication, som inte täcks av denna dokumentation. 
