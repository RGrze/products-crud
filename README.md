# EuroCert - zadanie rekrutacyjne

## Uruchomienie

Projekt najszybciej jest uruchomić przez docker-compose. Wystarczy wykonać komendę:

```bash
docker-compose up -d --build backend
```

Do aplikacji podpięta jest baza SQLite z załadowanymi 100 produktami. 
Produkty mają przypięte losowo kategorie nazwane "label 1", "label 2", "label 3", a niektóre
produkty mają przypisane więcej niż jedną kategorię.


Po uruchomieniu aplikacji dostępna jest dokumentacja openAPI pod adresem http://0.0.0.0:8000/docs
w której można testować endpointy.



Dostępny użytkownik:

```
username: user
API key: LlzyQg
```

Wymagane jest podanie w nagłówku `X-Api-Key` aby możliwe było 
korzystanie z API przedmiotów.
