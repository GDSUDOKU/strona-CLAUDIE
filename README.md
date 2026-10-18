# Dymczak Legal — strona dymczaklegal.com

Statyczna strona (HTML/CSS/JS) w trzech językach: `/pl/`, `/en/`, `/de/`.
Bez cookies, bez zewnętrznych skryptów i czcionek (Inter i Caladea są w `assets/fonts/`).

## Zanim opublikujesz

1. Otwórz `build.py` i uzupełnij sekcję `CONFIG` (adres e-mail, adres, NIP, izba, numer wpisu, OC, opcjonalnie telefon i miasto).
2. Uruchom `python3 build.py` — skrypt generuje wszystkie strony od nowa.
   Braki na stronie „Informacje prawne" są oznaczone żółtym `[…]`, a skrypt wypisuje ich listę.
3. Podgląd lokalny: `python3 -m http.server 8000` i wejdź na http://localhost:8000/

Teksty wszystkich wersji językowych są w `build.py` (słownik `T` oraz funkcja `legal_html`).

## Publikacja na GitHub Pages

1. Utwórz repozytorium (publiczne, np. `dymczaklegal`) i wgraj całą zawartość tego folderu (plik `CNAME` ma być w głównym katalogu).
2. Repozytorium → **Settings → Pages** → *Build and deployment*: Source = **Deploy from a branch**, branch = `main`, folder = `/ (root)`.
3. Tamże, w polu **Custom domain**, wpisz `dymczaklegal.com` i zapisz.
4. Skonfiguruj DNS (poniżej).
5. Gdy GitHub potwierdzi domenę, zaznacz **Enforce HTTPS** (certyfikat może pojawić się do 24 godzin po zmianie DNS).

Zalecane przed zmianą DNS: zweryfikuj domenę w ustawieniach konta GitHub (**Settings → Pages → Add a domain**), co chroni przed przejęciem domeny.

## DNS (u rejestratora domeny)

Usuń domyślne rekordy parkingowe, a potem dodaj:

| Typ   | Nazwa (host) | Wartość |
|-------|--------------|---------|
| A     | `@`          | `185.199.108.153` |
| A     | `@`          | `185.199.109.153` |
| A     | `@`          | `185.199.110.153` |
| A     | `@`          | `185.199.111.153` |
| AAAA  | `@`          | `2606:50c0:8000::153` |
| AAAA  | `@`          | `2606:50c0:8001::153` |
| AAAA  | `@`          | `2606:50c0:8002::153` |
| AAAA  | `@`          | `2606:50c0:8003::153` |
| CNAME | `www`        | `TWOJ-LOGIN.github.io` |

- `TWOJ-LOGIN` to nazwa użytkownika (lub organizacji) na GitHubie, bez nazwy repozytorium.
- Nie używaj rekordów wildcard (`*`).
- Jeśli rejestrator oferuje ALIAS/ANAME dla `@`, możesz użyć jednego rekordu `ALIAS` → `TWOJ-LOGIN.github.io` zamiast rekordów A/AAAA.
- Zmiany DNS propagują się do 24 godzin (zwykle znacznie szybciej).

Sprawdzenie (terminal):

    dig dymczaklegal.com +noall +answer -t A
    dig www.dymczaklegal.com +noall +answer

## Poczta na własnej domenie

Strona wyświetla adres z `CONFIG["email"]`. Jeśli chcesz używać adresu `@dymczaklegal.com`, potrzebujesz usługi poczty (np. u rejestratora lub w Google Workspace / Microsoft 365) i rekordów MX/SPF/DKIM — to osobna konfiguracja DNS, niezależna od GitHub Pages.

## Struktura

    index.html              wybór języka + automatyczne przekierowanie
    pl/ en/ de/             strona główna + informacje prawne w każdym języku
    assets/                 css, js, czcionki, zdjęcia
    build.py                generator (edytuj teksty i CONFIG tutaj)
    CNAME, robots.txt, sitemap.xml, 404.html, favicon.svg

## Dlaczego `www.dymczaklegal.com` może nie działać

Rekordy A/AAAA dla `@` obsługują tylko adres bez `www`. Adres z `www` jest osobną nazwą w DNS i potrzebuje własnego rekordu:

| Typ   | Nazwa | Wartość |
|-------|-------|---------|
| CNAME | `www` | `TWOJ-LOGIN.github.io` |

- Jeśli u rejestratora istnieje już rekord `www` (A lub CNAME wskazujący na hosting/parking), usuń go. Dla jednej nazwy nie może być CNAME i innego rekordu jednocześnie.
- Wartość to sama nazwa użytkownika na GitHubie + `.github.io`, bez nazwy repozytorium i bez `https://`.
- Przy ustawionej domenie `dymczaklegal.com` w GitHub Pages GitHub sam przekieruje `www` na wersję bez `www`.
- Po dodaniu rekordu poczekaj na propagację (zwykle do godziny, czasem do 24 h); certyfikat HTTPS dla `www` pojawia się dopiero po poprawnym sprawdzeniu DNS.
- Sprawdzenie: `dig www.dymczaklegal.com +noall +answer` powinno pokazać CNAME na `TWOJ-LOGIN.github.io`.
