# EuroCert - zadanie rekrutacyjne

## Uruchomienie

Projekt najszybciej jest uruchomić przez docker-compose. Wystarczy wykonać komendę:

```bash
docker-compose up -d --build backend
```

Do aplikacji podpięta jest baza SQLite z załadowanymi 100 produktami.


Dostępny użytkownik:

```
username: user
API key: LlzyQg
```

Wymagane jest podanie w nagłówku `X-Api-Key` aby możliwe było 
korzystanie z API przedmiotów.