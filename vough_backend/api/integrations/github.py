"""GitHub API

This module contains a class that hits the public GitHub API to search for organizations
using the provided given login name, and is also has a function to return the number of
public members of that organization.

It utilize the standard requests library.

"""
import os
import requests


class GithubApi:
    """
    API for returning pythonified GitHub organization data from the official GitHub API in json.

    ...

    Methods
    -------
    get_organization(request,  login: str)
        Attempts to retrieve the GitHub organization data with the given
        login name.
    get_organization(request,  login: str)
        Attempts to retrieve the number of GitHub organization members with the given
        login name.
    """
    API_URL = os.environ.get("GITHUB_API_URL", "https://api.github.com")
    GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")

    def get_organization(self, login: str):
        """Busca uma organização no Github

        :login: login da organização no Github
        """
        response = requests.get(self.API_URL + "/orgs/" + login)
        return response

    def get_organization_public_members(self, login: str) -> int:
        """Retorna todos os membros públicos de uma organização

        :login: login da organização no Github
        """
        response = requests.get(self.API_URL + "/orgs/" + login + "/members")
        return len(response.json())
