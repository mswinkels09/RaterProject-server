"""Module to show - What are the top five games by rating?"""
from gamerraterapi.models.gamerating import GameRating
import sqlite3
from django.shortcuts import render
from gamerraterapi.models import Game
from gamerraterreports.views import Connection


def topgames_list(request):
    """Function to build an HTML report of top 5 games by rating"""
    if request.method == 'GET':
        # Connect to project database
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            # Query for all events, with related user info.
            #Need refractoring to include Avg rating
            db_cursor.execute("""
                SELECT g.title GameTitle,
                    MAX(gra.rating) GameRating
                    FROM gamerraterapi_game g
                        JOIN gamerraterapi_gamerating gra On g.id = gra.game_id
                        GROUP BY GameTitle
                        ORDER BY GameRating Desc
                        LIMIT 5
            """)

            dataset = db_cursor.fetchall()

            # Take the flat data from the database, and build the
            # following data structure for each gamer.
            #
            # {
            #     1: {
            #         "id": 1,
            #         "full_name": "Admina Straytor",
            #         "games": [
            #             {
            #                 "id": 1,
            #                 "title": "Foo",
            #                 "maker": "Bar Games",
            #                 "skill_level": 3,
            #                 "number_of_players": 4,
            #                 "gametype_id": 2
            #             }
            #         ]
            #     }
            # }

            games_by_rating = {}

            for row in dataset:
                # Crete a Game instance and set its properties
                game = Game()
                game.title = row["GameTitle"]
                gameRating = GameRating()
                gameRating.rating = row["Gamerating"]

                # Store the user's id
                gametitle = row["GameTitle"]

                # If the user's id is already a key in the dictionary...
                if gametitle in games_by_rating:

                    # Add the current game to the `games` list for it
                    games_by_rating[gametitle]['games'].append(game)

                else:
                    # Otherwise, create the key and dictionary value
                    games_by_rating[gametitle] = {}
                    #["Title"] is what is being sent to the html.(BackEnd)
                    #gameTitle is the data that is represented in html.(FrontEnd)
                    games_by_rating[gametitle]["Title"] = gametitle 
                    games_by_rating[gametitle]["games"] = [game]
                    games_by_rating[gametitle]["GameRating"] = row["GameRating"]

        # Get only the values from the dictionary and create a list from them
        top_5_games_by_rating = games_by_rating.values()

        # Specify the Django template and provide data context
        template = 'list_with_top_games.html'
        context = {
            'topgames_list': top_5_games_by_rating
        }

        return render(request, template, context)