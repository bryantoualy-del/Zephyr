from pathlib import Path
p=Path('index.html')
s=p.read_text()
s=s.replace("+' jusqu'à la fin du tour de l'attaquant.'", "+\" jusqu'à la fin du tour de l'attaquant.\"")
s=s.replace("'Réaction • CON DD 15 • en cas d'échec, attaque à désavantage.'", "\"Réaction • CON DD 15 • en cas d'échec, attaque à désavantage.\"")
p.write_text(s)
