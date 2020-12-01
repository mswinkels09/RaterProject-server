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
            #         "GameTitle": "Clue",
            #         "GameRating": 5
            #     }
            # }


        # Specify the Django template and provide data context
        template = 'list_with_top_games.html'
        context = {
            'topgames_list': dataset
        }

        return render(request, template, context)