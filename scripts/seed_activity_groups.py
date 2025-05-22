# scripts/seed_activity_groups.py

from units.models import ActivityGroup

# On se base sur les choix CATEGORIES du modèle pour créer un groupe par catégorie
for key, label in ActivityGroup.CATEGORIES:
    group, created = ActivityGroup.objects.get_or_create(
        nom=label,
        defaults={
            "description": "",
            "categorie": key
        }
    )
    print(f"{'Created' if created else 'Exists '} — {group.nom} ({group.categorie})")
