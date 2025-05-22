import json
from geodata.models import Quartier

with open('geodata/quartiers_niamey.geojson', encoding='utf-8') as f:
    data = json.load(f)

for feature in data["features"]:
    nom = feature["properties"].get("nom")
    geom = feature["geometry"]
    if not nom:
        print("Quartier sans nom, ignoré")
        continue
    obj, created = Quartier.objects.get_or_create(nom=nom, defaults={"geom": geom})
    if created:
        print(f"Quartier ajouté : {nom}")
    else:
        print(f"Quartier déjà existant : {nom}")
