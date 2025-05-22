# scripts/seed_units.py

from units.models import Unite

units_by_type = {
    'cp': [
        'NIAMEY 2000',
        'TALLADJE',
        'SPJA/CCN',
        'FRANCOPHONIE',
        'KOUBIA',
        'RIVE DROITE',
        'BOUKOKI',
        'KIRKISSOYE',
        'ROUTE KOLLO',
        'AEROPORT',
        'YANTALA',
    ],
    'csp': [
        'WADATA',
        'STADE',
        'GRAND MARCHE',
    ],
    'pp': [
        'PETIT MARCHE',
        'MARCHE BONKANEY',
        'NOUVEAU MARCHE',
    ],
    'ui': [
        'BAC',
        'CU',
        'UPS',
    ],
    'constat': [
        'SERVICE CONSTAT',
    ],
    'upr': [
        'SERVICE UPR',
    ],
}

for type_code, names in units_by_type.items():
    for name in names:
        unite, created = Unite.objects.get_or_create(
            nom=name,
            defaults={'type': type_code}
        )
        if not created and unite.type != type_code:
            unite.type = type_code
            unite.save()
        print(f"{'Created' if created else 'Exists '} — {unite.nom} ({unite.type})")
