# scripts/seed_unit_groups.py

from units.models import Unite, ActivityGroup, UniteActivityGroup

all_units  = Unite.objects.all()
all_groups = ActivityGroup.objects.all()

for unit in all_units:
    for group in all_groups:
        uag, created = UniteActivityGroup.objects.get_or_create(
            unite=unit,
            group=group
        )
        print(f"{'Created' if created else 'Exists '} — {unit.nom} → {group.nom}")
