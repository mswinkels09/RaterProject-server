SELECT c.label CategoryLabel,
    Count(gc.game_id) CountOfGames
From gamerraterapi_category c
    Left Join gamerraterapi_gamecategory c On gc.category_id = c.id
    Group by CategoryLabel



