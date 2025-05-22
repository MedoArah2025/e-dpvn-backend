# activities/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.export_stats import ExportStatsView
from .views.stats import StatisticsByUnitView, StatisticsGlobalView, StatisticsGlobalFlatView
from .views.administratif import (
    AutresDeclarationsViewSet,
    ProcurationViewSet,
    DeclarationPerteViewSet,
    ResidenceViewSet,
    CinViewSet,
    AmendeForfaitaireViewSet,
)
from .views.circulation import (
    EnginImmobiliseViewSet,
    PieceRetireViewSet,
    VitreTeinteeViewSet,
)
from .views.constat import AccidentCirculationViewSet as ConstatAccidentViewSet
from .views.judiciaire import (
    PersonnesInterpelleViewSet,
    GavViewSet,
    DeferementViewSet,
    PlainteViewSet,
    DeclarationVolViewSet,
    InfractionViewSet,
    SaisieDrogueViewSet,
    AutreSaisieViewSet,
    RequisitionViewSet,
    IncendieViewSet,
    NoyadeViewSet,
    DecouverteCadavreViewSet,
    PersonnesEnleveViewSet,
    VehiculeEnleveViewSet,
    InfractionsGroupByQuartier,  # <-- bien importé ici !
)
from .views.dispositions import (
    MiseslctCtoViewSet,
    MiseDPJViewSet,
    MiseDispositionOcritViewSet,
    MiseDispositionDouaneViewSet,
    MiseDSTViewSet,
    MiseDPMFViewSet,
    MisePavillonEViewSet,
    MiseSonilogaViewSet,
)
from .views.operations import (
    PositionnementViewSet,
    ServiceOrdreViewSet,
    PatrouilleViewSet,
    CoupPoingViewSet,
    RaffleViewSet,
    DescenteViewSet,
)
from .views.rh import EffectifRHViewSet
from .views.test import TestAPIView
from .views.circulation import (
    EnginImmobiliseViewSet,
    PieceRetireViewSet,
    VitreTeinteeViewSet,
    ControleRoutierViewSet,   # ← AJOUTE-LE ICI
)
from .views.spja import MiseADispositionSpjaViewSet
router = DefaultRouter()

# Administratif
router.register(r'administratif/autres-declarations', AutresDeclarationsViewSet, basename='autres-declarations')
router.register(r'administratif/procurations', ProcurationViewSet, basename='procuration')
router.register(r'administratif/declarations-perte', DeclarationPerteViewSet, basename='declaration-perte')
router.register(r'administratif/residences', ResidenceViewSet, basename='residence')
router.register(r'administratif/cin', CinViewSet, basename='cin')
router.register(r'administratif/amendes-forfaitaires', AmendeForfaitaireViewSet, basename='amende-forfaitaire')

# Circulation
router.register(r'circulation/engin-immobilises', EnginImmobiliseViewSet, basename='engin-immobilise')
router.register(r'circulation/pieces-retirees', PieceRetireViewSet, basename='piece-retiree')
router.register(r'circulation/vitres-teintees', VitreTeinteeViewSet, basename='vitre-teintee')

# Constat
router.register(r'constats', ConstatAccidentViewSet, basename='constat')

# Judiciaire
router.register(r'judiciaire/interpellations', PersonnesInterpelleViewSet, basename='interpellations')
router.register(r'judiciaire/gav', GavViewSet, basename='gav')
router.register(r'judiciaire/deferements', DeferementViewSet, basename='deferements')
router.register(r'judiciaire/plainte', PlainteViewSet, basename='plainte')
router.register(r'judiciaire/declaration-vols', DeclarationVolViewSet, basename='declaration-vols')
router.register(r'judiciaire/infractions', InfractionViewSet, basename='infractions')
router.register(r'judiciaire/saisie-drogue', SaisieDrogueViewSet, basename='saisie-drogue')
router.register(r'judiciaire/autres-saisies', AutreSaisieViewSet, basename='autres-saisies')
router.register(r'judiciaire/requisitions', RequisitionViewSet, basename='requisitions')
router.register(r'judiciaire/incendies', IncendieViewSet, basename='incendies')
router.register(r'judiciaire/noyades', NoyadeViewSet, basename='noyades')
router.register(r'judiciaire/decouvertes-cadavre', DecouverteCadavreViewSet, basename='decouvertes-cadavre')
router.register(r'judiciaire/enlevements', PersonnesEnleveViewSet, basename='enlevements-personnes')
router.register(r'judiciaire/vehicules-enleves', VehiculeEnleveViewSet, basename='enlevements-vehicules')

# Dispositions
router.register(r'dispositions/slct-cto', MiseslctCtoViewSet, basename='slct-cto')
router.register(r'dispositions/dpj', MiseDPJViewSet, basename='dpj')
router.register(r'dispositions/ocr-im', MiseDispositionOcritViewSet, basename='ocr-im')
router.register(r'dispositions/douane', MiseDispositionDouaneViewSet, basename='douane')
router.register(r'dispositions/dst', MiseDSTViewSet, basename='dst')
router.register(r'dispositions/dpmf', MiseDPMFViewSet, basename='dpmf')
router.register(r'dispositions/pavillon-e', MisePavillonEViewSet, basename='pavillon-e')
router.register(r'dispositions/soniloga', MiseSonilogaViewSet, basename='soniloga')

# Opérations
router.register(r'operations/positionnements', PositionnementViewSet, basename='positionnements')
router.register(r'operations/services-ordre', ServiceOrdreViewSet, basename='services-ordre')
router.register(r'operations/patrouilles', PatrouilleViewSet, basename='patrouilles')
router.register(r'operations/coups-poing', CoupPoingViewSet, basename='coups-poing')
router.register(r'operations/raffles', RaffleViewSet, basename='raffles')
router.register(r'operations/descente', DescenteViewSet, basename='descente')

# Ressources Humaines
router.register(r'rh/effectifs', EffectifRHViewSet, basename='effectifs-rh')
router.register(r'circulation/controles-routiers', ControleRoutierViewSet, basename='controle-routier')
router.register(r'spja/mises-a-disposition', MiseADispositionSpjaViewSet, basename='mises-a-disposition-spja')
urlpatterns = [
path(
        "judiciaire/infractions/group_by_quartier/",
        InfractionsGroupByQuartier.as_view(),
        name="infractions-group-by-quartier",
    ),
    path('', include(router.urls)),
    # Exports & Stats
    path("statistics/units/<int:unit_id>/export/", ExportStatsView.as_view(), name="export-stats-unit"),
    path("statistics/units/<int:unit_id>/", StatisticsByUnitView.as_view(), name="stats-unit"),
    path("statistics/global/", StatisticsGlobalView.as_view(), name="stats-global"),
    path("statistics/export/", ExportStatsView.as_view(), name="export-stats-global"),
    path("statistics/global/flat/", StatisticsGlobalFlatView.as_view(), name="statistics-global-flat"),
    # Carte Infractions PRO
    #path("judiciaire/infractions/group_by_quartier/", InfractionsGroupByQuartier.as_view(), name="infractions-group-by-quartier"),

    path("test-endpoint/", TestAPIView.as_view(), name="test-endpoint"),

]
