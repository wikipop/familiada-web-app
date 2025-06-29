# Familiada - Gra Rodzinna

Interaktywna aplikacja do gry w Familiadę, stworzona przy użyciu Vue 3, TypeScript, Vite, Tailwind CSS i shadcn/vue.
![Podgląd](assets/preview.png)

> **Podgląd online:**  
> Aplikacja jest dostępna w wersji demonstracyjnej pod adresem: [familiada31lo.wyniki.zip/](https://familiada31lo.wyniki.zip/)

## Funkcje

- Panel administratora do zarządzania pytaniami i odpowiedziami
- Tablica gry dla graczy i publiczności
- Synchronizacja stanu między panelem administratora a tablicą gry za pomocą localStorage
- Animacje odkrywania odpowiedzi
- Wskaźniki błędów (X)
- Efekty dźwiękowe (opcjonalne)

## Wymagania

- Node.js (wersja 14 lub nowsza)
- Yarn lub npm

## Instalacja

1. Sklonuj repozytorium
2. Zainstaluj zależności:

```bash
cd familiada-app

# npm
npx install
# yarn
yarn install
```

## Uruchamianie aplikacji

### npm
Zbuduj i serwuj aplikację:
```bash
npx build
npx preview
```
lub poprostu odpal serwer developerski
```bash
npx dev
```

### yarn
Zbuduj i serwuj aplikację:
```bash
yarn build
yarn preview
```
lub poprostu odpal serwer developerski
```bash
yarn dev
```

Aplikacja będzie dostępna pod adresem: http://localhost:5173/

## Ścieżki aplikacji

- **/admin** - Panel administratora do zarządzania grą
- **/game** - Tablica gry dla graczy i publiczności

## Jak grać

1. Otwórz ścieżkę **/admin** w jednej karcie przeglądarki
2. Otwórz ścieżkę **/game** w drugiej karcie przeglądarki (najlepiej na innym ekranie widocznym dla graczy)
3. W panelu administratora wybierz pytanie i kliknij "Rozpocznij grę"
4. Odkrywaj odpowiedzi klikając przycisk "Odkryj" obok każdej odpowiedzi
5. Dodawaj błędy (X) klikając przycisk "Dodaj X"
6. Resetuj grę klikając przycisk "Resetuj grę"

## Efekty dźwiękowe

Aby dodać efekty dźwiękowe, umieść pliki dźwiękowe w katalogu `public/sounds/`:
- `reveal.mp3` - dźwięk odtwarzany przy odkrywaniu odpowiedzi
- `strike.mp3` - dźwięk odtwarzany przy dodawaniu błędu (X)

## Dostosowywanie pytań

Pytania i odpowiedzi są przechowywane w pliku `public/data/familiada_pytania.json`. Możesz edytować ten plik, aby dodać własne pytania i odpowiedzi.

W repo jest też skrypt, który automatycznie konwertuje pytania z csv do jsona i punktuje je (pomocne w przypadku małej 
próby ankiety), aby go użyć, przygotuj pytania w tabeli w [takim formacie](https://docs.google.com/spreadsheets/d/1tezt8hgNLtGwNgMyhBrUlY2FUZ1j6iLHH0yGvZl-X1w/edit?usp=sharing)
i podmień plik `/data/familiada_pytania.csv` na swój własny.

## Technologie

- Vue 3
- TypeScript
- Vite
- Tailwind CSS
- shadcn/vue
- Vue Router
