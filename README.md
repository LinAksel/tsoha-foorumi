# Keskustelufoormi Sipsitys

Helsingin yliopiston Tietokantasovellus-kurssin harjoitustyönä toteutettava ohjelma.

## Heroku

* [Foorumi](https://tsoha2020-foorumi.herokuapp.com/)

## Kuvaus

Sipsitys on keskustelufoorumi, jossa sisäänkirjautunut käyttäjä voi selata eri aihepiireihin jaettuja (sipsiaiheisia) viestejä, sekä lisätä niitä.
Uudenlaisia aihelisäyksiä on myös mahdollista ehdottaa admineille. Tulevaisuudessa käyttäjä voi myös lisätä tietoa itsestään profiilisivulle, valita viestin lähetyksen kohdalla kaikki siihen sopivat aiheet kerralla, ja liputtaa muiden käyttäjien viestejä.

## Toiminnallisuudet 18.10.2020

* Käyttäjä voi rekisteröityä sivulle tunnuksella, joka ei ole jo varattu
* Käyttäjä voi kirjautua olemassaolevalla tunnuksella
* Käyttäjä näkee kymmenen suosituinta aihetta palkissa
* Käyttäjä voi selata kaikkia aiheita
* Sisäänkirjautunut käyttäjä voi liputtaa viestejä
* Sisäänkirjautunut käyttäjä voi poistaa oman viestinsä
* Sisäänkirjautunut käyttäjä voi muokata omaa viestiään
* Sisäänkirjautunut käyttäjä voi lukea aihealueiden viestejä
* Sisäänkirjautunut käyttäjä voi lisätä aihealueelle viestin
* Sisäänkirjautunut käyttäjä voi ehdottaa uutta aihetta

## Puuttuva toiminnallisuus 5.10.2020 (todo ennen loppupalautusta)

* Käyttäjä voi nähdä profiilinsa (osittain kesken)
* Käyttäjä voi lisätä tietoa profiiliinsa, ja poistaa sitä
* Käyttäjä voi tallentaa suosikkiviestejään
* Erilaiset käyttäjäroolit peruskäyttäjän lisäksi:
    * Admin: voi poistaa tai lisätä viestin, aiheen tai käyttäjän,
    sekä nähdä aihe-ehdotukset. Näkee lisäksi viestien liputusmäärät ja liputtajat
    * Moderaattori: voi poistaa viestejä, ja näkee viestien liputusmäärät sekä liputtajat.

## Lisädokumentaatio

* [Välipalautuskommentit (SISÄLTÄÄ KYSYMYKSIÄ TARKASTAJALLE!!)](/docs/valipalautukset.md)
* [Alkuperäinen määrittely (PÄIVITETÄÄN)](/docs/maarittelydoc.md)
