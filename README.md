# Keskustelusovellus

Tietokantasovellusten harjoitustyönä toteutettu web-keskustelupalsta.

## Sovelluksen toiminnallisuudet

Sovelluksen ominaisuudet on otettu kurssilla ehdotetusta aiheesta lähes sellaisenaan.

Sovelluksessa näkyy keskustelualueita, joista jokaisella on otsikko ja kuvaus, jotka kertovat aiheen. Alueet sisältävät viesteistä muodostuvia keskusteluketjuja. Jokainen käyttäjä on peruskäyttäjä tai ylläpitäjä.

Toiminnallisuudet:
- Käyttäjä voi luoda uuden tunnuksen.
- Käyttäjä voi kirjautua sisään ja ulos.
- Käyttäjä näkee sovelluksen etusivulla listan alueista.
- Käyttäjä näkee jokaisen alueen ketjujen ja viestien määrän.
- Käyttäjä näkee jokaisen alueen viimeksi lähetetyn viestin ajankohdan.
- Käyttäjä voi luoda alueelle uuden ketjun antamalla ketjun otsikon ja aloitusviestin sisällön.
- Käyttäjä voi kirjoittaa uuden viestin olemassa olevaan ketjuun.
- Käyttäjä voi muokata luomansa ketjun otsikkoa sekä lähettämänsä viestin sisältöä.
- Käyttäjä voi myös poistaa itse luomansa ketjun tai viestin.
- Käyttäjä voi etsiä kaikki viestit, joiden osana on annettu sana.
- Ylläpitäjä voi poistaa minkä tahansa ketjun tai viestin.
- Ylläpitäjä voi lisätä ja poistaa keskustelualueita.
- Ylläpitäjä voi luoda salaisen alueen ja määrittää, keillä käyttäjillä on pääsy alueelle.

## Käyttö

Sovellus on saatavilla https://tsoha-forum.fly.dev/ . Siihen voi kirjautua valmiilla tileillä `admin:tsoha1` ja `user:tsoha2`, joista ensimmäisellä on ylläpitäjän oikeudet. Käytön alussa saattaa tulla virheilmoitus, joka johtunee tietokannan käynnistymisviiveestä.

Vaihtoehtoinen paikallinen asennusohje Linuxille:
- Kloonaa tämä repositorio.
- Luo `.env`-tiedosto repositorin juurikansioon.
- Lisää `.env`-tiedostoon rivit muotoa `DATABASE_URL=<tietokannan osoite>` ja `SECRET_KEY=<salainen_avain>`.
- Asenna virtuaaliympäristö komennolla `python3 -m venv .venv` ja aktivoi komennolla `source .venv/bin/activate`.
- Lataa sovelluksen riippuvuudet komennolla `pip install -r requirements.txt`
- Määritä tietokannan skeema komennolla `psql < schema.sql`
- Käynnistä sovellus komennolla `flask run`.

Jos sovelluksella ei ole yhtään käyttäjää, ensimmäinen siihen lisätty tili saa pääkäyttäjän oikeudet.
