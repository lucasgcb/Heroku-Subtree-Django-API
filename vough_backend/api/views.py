from rest_framework import viewsets, status
from rest_framework.views import Response
from django.http import Http404
from api import models, serializers
from api.integrations.github import GithubApi
from api.models import Organization
import json

# TODOS:
# 1 - Buscar organização pelo login através da API do Github
# 2 - Armazenar os dados atualizados da organização no banco
# 3 - Retornar corretamente os dados da organização
# 4 - Retornar os dados de organizações ordenados pelo score na listagem da API


class OrganizationViewSet(viewsets.ModelViewSet):

    queryset = models.Organization.objects.all().order_by('-score')
    serializer_class = serializers.OrganizationSerializer
    lookup_field = "login"

    def retrieve(self, request, login=None):
        API = GithubApi()
        r = API.get_organization(login)
        if r.ok: 
            json = r.json()
            try:
                name = json["name"]
            except:
                name = json["login"]
            
            score = json["public_repos"] + API.get_organization_public_members(login)
            b = Organization(login=json["login"], name=name, score=score)
            b.save()
            return Response(json)
        raise Http404
