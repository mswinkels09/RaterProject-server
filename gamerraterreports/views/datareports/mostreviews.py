"""Module to show - game with the most reviews"""
import sqlite3
from django.shortcuts import render
from gamerraterreports.views import Connection


def mostreviewedgame_list(request):
    """Function to build an HTML report of the game with the most reviews"""
    if request.method == 'GET':
        # Connect to project database
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            db_cursor.execute("""
                SELECT GameTitle,
                    Max(NumOfReviews) HighestNumReviews
                From (
                    Select
                        g.title GameTitle,
                        Count(gre.id) NumOfReviews
                    From gamerraterapi_game g
                        JOIN gamerraterapi_gamereview gre ON g.id = gre.game_id
                        GROUP By GameTitle
                )
            """)

            dataset = db_cursor.fetchall()

            # Take the flat data from the database, and build the
            # following data structure for each gamer.
            #
            # {
            #     1: {
            #         "id": 1,
            #         "GameTitle": "Oregon Trail",
            #         "HighestNumReviews": 2
            #     }
            # }


        # Specify the Django template and provide data context
        template = 'list_most_reviewed_game.html'
        context = {
            'mostreviewedgame_list': dataset
        }

        return render(request, template, context)