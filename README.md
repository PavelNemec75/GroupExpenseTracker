# GroupExpenseTracker

verze neresi:

- frontend
- zaokrouhlovani
- komunikaci emailem
- *** autentikaci - google, django all-auth?
- autentikaci pres vice provideru
- *** strawberry dataloadery
- *** docker compose - zvlast kontejner pro django aplikaci a zvlast volume pro db
- skalovani
- *** vykonnost databaze - indexy
- *** strankovani
- autorizaci
- lokalizaci
- nelze smazat participant pokud ma zaznam v event_expense_group
zde by sla pridat dalsi logika - napr. lze smazat pokud je jeho bilance nulova atd.
- validace emailove adresy
- nezobrazovat detailni chybove hlasky v produkcnim rezimu
- komentare v kodu
- zprovoznit debug toolbar - ladeni ORM - SQL
- lepsi osetreni chyb misto raise ValueError vytvorit response objekty a vracet
- logika v models i schema - lepsi by bylo to sjednotit na jedno misto.?
- rozdeleni schema a mozna i models do vice souboru - prilis hodne radku.? 