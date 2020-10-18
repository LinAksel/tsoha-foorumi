# Keskustelufoormi Sipsitys

Helsingin yliopiston Tietokantasovellus-kurssin harjoitustyönä toteutettava ohjelma.

## Heroku

* [Foorumi](https://tsoha2020-foorumi.herokuapp.com/)

## Kuvaus

Sipsitys on keskustelufoorumi, jossa sisäänkirjautunut käyttäjä voi selata eri aihepiireihin jaettuja (sipsiaiheisia) viestejä, sekä lisätä niitä.
Uudenlaisia aihelisäyksiä on myös mahdollista ehdottaa admineille.

## Lopulliset toiminnallisuudet:

* Käyttäjä voi rekisteröityä sivulle tunnuksella, joka ei ole jo varattu

* Käyttäjä voi kirjautua olemassaolevalla tunnuksella

* Käyttäjä näkee kymmenen suosituinta aihetta palkissa

* Käyttäjä voi selata kaikkia aiheita

* Sisäänkirjautunut käyttäjä voi nähdä profiilinsa

* Sisäänkirjautunut käyttäjä voi lisätä tietoa profiiliinsa, ja muokata sitä

* Sisäänkirjautunut käyttäjä voi liputtaa viestejä

* Sisäänkirjautunut käyttäjä voi poistaa oman viestinsä

* Sisäänkirjautunut käyttäjä voi muokata omaa viestiään

* Sisäänkirjautunut käyttäjä voi lukea aihealueiden viestejä

* Sisäänkirjautunut käyttäjä voi lisätä aihealueelle viestin

* Sisäänkirjautunut käyttäjä voi ehdottaa uutta aihetta

* Moderaattori voi muokata kaikkia viestejä

* Ylläpitäjä voi poistaa minkä vain viestin

* Moderaattorit ja ylläpitäjät näkevät raportoidut viestit

## Lisäkommentit:

* Rakenne suunniteltu niin, että reittikerroksessa käsitellään oikeudet (onko sopiva käyttäjä) ja tietokantakerroksissa data (onko sopivaa dataa).

* Admin- ja moderaattoritunnukset loppuarviointia varten labtoolin edellisen palautuksen kommenteissa! Heroku on kuitenkin julkinen, joten parempi rajoittaa näiden saatavuutta.

* Aihe-ehdotuksia ei ikävä kyllä näe suoraan sivulta, tämä ominaisuus jäi "lähes valmiiksi", sillä tietokantayhteydet on jo tehty!

* Sivun tulisi olla suhteellisen selkeä ilman näitä suurempia kuvailuja, sillä kaikesta tulee asianmukainen virheviesti, mikäli jotain sopimatonta tehdään.