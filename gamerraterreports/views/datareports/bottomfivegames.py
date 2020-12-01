"""Module to show - What are the bottom five games by rating?"""
import sqlite3
from django.shortcuts import render
from gamerraterreports.views import Connection


def bottomgames_list(request):
    """Function to build an HTML report of bottom 5 games by rating"""
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
                        ORDER BY GameRating ASC
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
        template = 'list_with_bottom_games.html'
        context = {
            'bottomgames_list': dataset
        }

        return render(request, template, context)