"""
Views for the vough application.

"""

from rest_framework import viewsets
from rest_framework.views import Response
from django.http import Http404
from api import models, serializers
from api.integrations.github import GithubApi
from api.models import Organization

# TODOS:
# 1 - Buscar organização pelo login através da API do Github
# 2 - Armazenar os dados atualizados da organização no banco
# 3 - Retornar corretamente os dados da organização
# 4 - Retornar os dados de organizações ordenados pelo score na listagem da API


class OrganizationViewSet(viewsets.ModelViewSet):
    """
    Viewset for returning, scrapping and deleting API information of GitHub organizations.

    ...

    Methods
    -------
    retrieve(request, login=None)
        Attempts to retrieve, return and store GitHub organizations with the matching login.
        Returns json on hit.
        Throws 404 on miss.
    """
    # Ordenar por ordem decrescente (maior para menor)
    queryset = models.Organization.objects.all().order_by('-score')  # pylint: disable=no-member
    serializer_class = serializers.OrganizationSerializer
    lookup_field = "login"
    def retrieve(self, request, login=None):
        api = GithubApi()
        response = api.get_organization(login)
        if response.ok:
            json = response.json()
            try:
                name = json["name"] # Resposta por vir sem name!
                #Ex: /api/orgs/rebellionifsc
            except KeyError:
                name = json["login"]
            score = json["public_repos"] + api.get_organization_public_members(login)
            organization_update = Organization(login=json["login"], name=name, score=score)
            organization_update.save()
            return Response(json)
        raise Http404
