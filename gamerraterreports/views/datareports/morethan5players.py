"""Module to show - Games with more than 5 players"""
import sqlite3
from django.shortcuts import render
from gamerraterreports.views import Connection


def morethan5players_list(request):
    """Function to build an HTML report of Games with more than 5 players"""
    if request.method == 'GET':
        # Connect to project database
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            db_cursor.execute("""
                SELECT title,
                    num_of_players
                From gamerraterapi_game
                    Where num_of_players > 5;
            """)

            dataset = db_cursor.fetchall()

            # Take the flat data from the database, and build the
            # following data structure for each gamer.
            #
            # {
            #     1: {
            #         "id": 1,
            #         "CategoryLabel": "Strategy",
            #         "CountOfGames": 4
            #     }
            # }


        # Specify the Django template and provide data context
        template = 'list_games_more_than_5_players.html'
        context = {
            'morethan5players_list': dataset
        }

        return render(request, template, context)