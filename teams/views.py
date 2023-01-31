from rest_framework.views import APIView
from rest_framework.views import Request, Response
from django.forms.models import model_to_dict

from teams.models import Team
from utils import ImpossibleTitlesError, InvalidYearCupError, NegativeTitlesError, data_processing


class TeamView(APIView):
    def post(self, request: Request):
        try:
            data = request.data
            data_processing(data)

            response = Team.objects.create(**data)
            response_dict = model_to_dict(response)

            return Response(response_dict, 201)
        except (NegativeTitlesError, InvalidYearCupError, ImpossibleTitlesError) as error:
            return Response(error.message, 400)

    def get(self, request: Request):
        response = Team.objects.values()
        return Response(response, 200)


class TeamDetailView(APIView):
    def get(self, request: Request, team_id):
        try:
            response = Team.objects.get(id=team_id)

        except Team.DoesNotExist:
            return Response({"message": "Team not found"}, 404)

        response_dict = model_to_dict(response)
        return Response(response_dict, 200)

    def patch(self, request: Request, team_id):
        try:
            data = request.data.items()
            response = Team.objects.get(id=team_id)

            [setattr(response, key, value) for key, value in data]

            response.save()

        except Team.DoesNotExist:
            return Response({"message": "Team not found"}, 404)

        response_dict = model_to_dict(response)
        return Response(response_dict, 200)

    def delete(self, request: Request, team_id):
        try:
            response = Team.objects.get(id=team_id)

        except Team.DoesNotExist:
            return Response({"message": "Team not found"}, 404)

        response.delete()
        return Response(status=204)
