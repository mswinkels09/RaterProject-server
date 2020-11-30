"""View module for handling requests about games"""
from gamerraterapi.views.category import Categories, CategorySerializer
from gamerraterapi.models import category
from gamerraterapi.models.gamecategory import GameCategory
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from gamerraterapi.models import Game, Category

##your new games/request.py##

class Games(ViewSet):
    """Level up games"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized game instance
        """

        # Uses the token passed in the `Authorization` header
        user = User.objects.get(user=request.auth.user)

        # Create a new Python instance of the Game class
        # and set its properties from what was sent in the
        # body of the request from the client.
        game = Game()
        game.title = request.data["title"]
        game.description = request.data["description"]
        game.num_of_players = request.data["numberOfPlayers"]
        game.year_released = request.data["yearReleased"]
        game.est_time = request.data["estimatedTime"]
        game.age_rec = request.data["ageRecommendation"]
        game.designer = request.data["designer"]
        game.user = user

        # Use the Django ORM to get the record from the database
        # whose `id` is what the client passed as the
        # `gameTypeId` in the body of the request.
        # category = Category.objects.get(pk=request.data["categoryId"])
        # game.category = category

        # Try to save the new game to the database, then
        # serialize the game instance as JSON, and send the
        # JSON as a response to the client request
        try:
            game.save()
            serializer = GameSerializer(game, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # If anything went wrong, catch the exception and
        # send a response with a 400 status code to tell the
        # client that something was wrong with its request data
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)



    def retrieve(self, request, pk=None):
        """Handle GET requests for single game

        Returns:
            Response -- JSON serialized game instance
        """
        try:
            # `pk` is a parameter to this function, and
            # Django parses it from the URL route parameter
            #   http://localhost:8000/games/2
            #
            # The `2` at the end of the route becomes `pk`
            game = Game.objects.get(pk=pk)
            serializer = GameSerializer(game, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a game

        Returns:
            Response -- Empty body with 204 status code
        """

        # Do mostly the same thing as POST, but instead of
        # creating a new instance of Game, get the game record
        # from the database whose primary key is `pk`
        game = Game.objects.get(pk=pk)
        game.title = request.data["title"]
        game.description = request.data["description"]
        game.num_of_players = request.data["numberOfPlayers"]
        game.year_released = request.data["yearReleased"]
        game.est_time = request.data["estimatedTime"]
        game.age_rec = request.data["ageRecommendation"]
        game.designer = request.data["designer"]

        category = Category.objects.get(pk=request.data["categoryId"])
        game.category = category

        game.save()

        # 204 status code means everything worked but the
        # server is not sending back any data in the response
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single game

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            game = Game.objects.get(pk=pk)
            game.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Game.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to games resource

        Returns:
            Response -- JSON serialized list of games
        """
        # Get all game records from the database
        #SELECT * FROM levelupapi_game
        games = Game.objects.all()

        # Support filtering games by type
        #    http://localhost:8000/games?type=1
        #
        # That URL will retrieve all tabletop games
        # categories = self.request.query_params.get('categoryId', None)
        # if categories is not None:
        #     games = games.filter(category__id=type)

        serializer = GameSerializer(
            games, many=True, context={'request': request})
            ## Response = sends data in parentheses to client in JSON
        return Response(serializer.data)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields=['label', ]

class GameCategorySerializer(serializers.ModelSerializer):
    """JSON serializer for event organizer's related Django user"""
    category = CategorySerializer(many=False)

    class Meta:
        model = GameCategory
        fields = ['category', ]

##sends a url with each individual game
class GameSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for games

    Arguments:
        serializer type
    """
    categories = GameCategorySerializer(many=True)
    ##Prepare data to be sent as JSON##
    class Meta:
        model = Game
        fields = ('id', 'url', 'categories', 'title', 'num_of_players', 'year_released', 'description', 'designer', 'est_time', 'age_rec')
        #nests the data
        depth = 1
