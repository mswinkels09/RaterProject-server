"""Module to show - Number of Games per Category"""
from gamerraterapi.models.category import Category
import sqlite3
from django.shortcuts import render
from gamerraterapi.models import Game
from gamerraterreports.views import Connection


def gamespercategory_list(request):
    """Function to build an HTML report of top 5 games by rating"""
    if request.method == 'GET':
        # Connect to project database
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            #Left Join takes all the data from one table 
            #even if the table joining in doesnt have matching data
            db_cursor.execute("""
                SELECT c.label CategoryLabel,
                    Count(gc.game_id) NumOfGames
                From gamerraterapi_category c
                    Left Join gamerraterapi_gamecategory gc On gc.category_id = c.id
                    Group by CategoryLabel
                    Order By NumOfGames Desc
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
        template = 'list_games_per_category.html'
        context = {
            'gamespercategory_list': dataset
        }

        return render(request, template, context)