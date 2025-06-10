from apps.tutoriais.api.serializers import EtapaSerializer
from apps.tutoriais.api.serializers import MaterialSerializer
from apps.tutoriais.api.serializers import MaterialTutorialSerializer
from apps.tutoriais.api.serializers import TutorialSerializer
from apps.tutoriais.models import Etapa
from apps.tutoriais.models import Material
from apps.tutoriais.models import MaterialTutorial
from apps.tutoriais.models import Tutorial

from rest_framework.viewsets import ModelViewSet


class MaterialViewSet(ModelViewSet[Material]):
    """
    API endpoint that allows materials to be viewed or edited.
    """

    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
    http_method_names = ["get", "post", "put", "delete"]


class TutorialViewSet(ModelViewSet[Tutorial]):
    """
    API endpoint that allows tutorials to be viewed or edited.
    """

    queryset = Tutorial.objects.all()
    serializer_class = TutorialSerializer
    http_method_names = ["get", "post", "put", "delete"]


class MaterialTutorialViewSet(ModelViewSet[MaterialTutorial]):
    """
    API endpoint that allows material-tutorial relationships to be viewed or edited.
    """

    queryset = MaterialTutorial.objects.all()
    serializer_class = MaterialTutorialSerializer
    http_method_names = ["get", "post", "put", "delete"]


class EtapaViewSet(ModelViewSet[Etapa]):
    """
    API endpoint that allows etapas to be viewed or edited.
    """

    queryset = Etapa.objects.all()
    serializer_class = EtapaSerializer
    http_method_names = ["get", "post", "put", "delete"]
