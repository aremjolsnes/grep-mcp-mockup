# Demo-prompter: Grep + MCP + Learner Context

Kjør disse én etter én i Claude Code-chatvinduet.

---

## Steg 1 – Uten Learner Context

```
Hvilke kompetansemål i samfunnsfag er relevante for et prosjekt om demokrati og valg på 10. trinn?
```

*Forventet: AI bruker grep_hent_kompetansemaal("SAF01-04", "10"), lister relevante KM. Korrekt, men generisk.*

---

## Steg 2 – Med Learner Context

```
Du er en pedagogisk assistent. Her er konteksten for denne klassen:

{
  "rolle": "lærer",
  "trinn": "10",
  "fag": "SAF01-04",
  "gjennomgaatt": ["KM1638", "KM1640", "KM1643"]
}

Hvilke kompetansemål i samfunnsfag er relevante for et prosjekt om demokrati og valg?
Ta hensyn til at de allerede gjennomgåtte målene ikke trenger å prioriteres.
```

*Forventet: AI bruker samme verktøy, men peker direkte på KM1648 og KM1652 som neste steg.*

---

## Steg 3 – CASE-format

```
Kan du hente de samme kompetansemålene i samfunnsfag for 10. trinn, men returnere dem i CASE-format?
```

*Forventet: AI bruker grep_hent_cfitems("SAF01-04", "10") og returnerer CFDocument + CFItems.*

---

## Steg 4 – Nevada-eksempelet (innspill fra internasjonal deltaker)

```
Jeg jobber med læreplandata fra Nevada, USA. En av standardene deres er:

  SS.9-12.CE.1 – "Understand the structure and function of government,
  including the U.S. Constitution, separation of powers, and the role
  of citizens in a democratic society."

Kan du finne norske kompetansemål i samfunnsfag for 10. trinn som dekker
tilsvarende forståelse, og vise hvordan de ville sett ut i CASE-format
slik at de to systemene kan sammenlignes?
```

*Forventet: AI bruker grep_hent_cfitems("SAF01-04", "10"), identifiserer KM1652 (og KM1648) som match, viser CASE-struktur for begge. Poeng: samme ambisjon – to systemer – én bro.*
