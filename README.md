# Keskustelusovellus

Tietokantasovellusten harjoitustyönä toteutettava web-keskustelupalsta.

## Sovelluksen ominaisuuksia

Sovelluksen ominaisuudet on otettu kurssilla ehdotetusta aiheesta lähes sellaisenaan. On tarkoitus, että sovellus sisältää vähintään nämä ominaisuudet, mutta ominaisuuksia voidaan tarvittaessa lisätä.

Sovelluksessa näkyy keskustelualueita, joista jokaisella on otsikko ja kuvaus, jotka kertovat aiheen. Alueet sisältävät viesteistä muodostuvia keskusteluketjuja. Jokainen käyttäjä on peruskäyttäjä tai ylläpitäjä.

Suunnitellut toiminnallisuudet:
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

## Sovelluksen tilanne

Sovellus sisältää seuraavat toiminnallisuudet:

- Käyttäjä voi luoda uuden tunnuksen.
- Käyttäjä voi kirjautua sisään ja ulos.
- Käyttäjä näkee sovelluksen etusivulla listan alueista.
- Käyttäjä voi luoda alueelle uuden ketjun antamalla ketjun otsikon ja aloitusviestin sisällön.
- Käyttäjä voi kirjoittaa uuden viestin olemassa olevaan ketjuun.
- Ylläpitäjä voi lisätä keskustelualueita.

Sovellus sisältää vasta minimaaliset ominaisuudet, jotka mahdollistavat viestien lähettämisen sovellukseen. Esimerkiksi mitään sisällön tarkastuksia ei ole vielä toteutettu.

## Käyttö

Sovellus on saatavilla https://tsoha-forum.fly.dev/ . Siihen voi kirjautua valmiilla tileillä `admin:tsoha1` ja `user:tsoha2`, joista ensimmäisellä on ylläpitäjän oikeudet.

Vaihtoehtoinen paikallinen asennusohje Linuxille:
- Kloonaa tämä repositorio.
- Luo `.env`-tiedosto repositorin juurikansioon.
- Lisää `.env`-tiedostoon rivit muotoa `DATABASE_URL=<tietokannan osoite>` ja `SECRET_KEY=<salainen_avain>`.
- Asenna virtuaaliympäristö komennolla `python3 -m venv .venv` ja aktivoi komennolla `source .venv/bin/activate`.
- Lataa sovelluksen riippuvuudet komennolla `pip install -r requirements.txt`
- Määritä tietokannan skeema komennolla `psql < schema.sql`
- Käynnistä sovellus komennolla `flask run`.



