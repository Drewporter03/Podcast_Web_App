from sqlalchemy import select, inspect
from podcast.adapters.orm import mapper_registry


# Test case to see if the tables name are bieng populated properly to the database
def test_database_populate_inspect_table_names(database_engine):
    # Get table information
    inspector = inspect(database_engine)
    assert inspector.get_table_names() == ['authors', 'categories', 'episodes', 'playlist', 'playlist_episodes',
                                           'podcast_categories', 'podcasts', 'reviews', 'users']


# Test case to see if the categories is being populated correctly to the database
def test_database_populate_categories(database_engine):
    inspector = inspect(database_engine)
    categories = inspector.get_table_names()[1]

    columns = inspector.get_columns(categories)
    column_names = [column['name'] for column in columns]

    with database_engine.connect() as connection:
        select_statement = select(mapper_registry.metadata.tables[categories])
        result = connection.execute(select_statement)
        categories_name = []
        for row in result:
            categories_name.append(row[1])
        assert categories_name[0:4] == ['Society & Culture', 'Personal Journals', 'Professional', 'News & Politics']
        # checking if all column are being initiated properly
        assert column_names ==  ['category_id', 'category_name']


# Test to see if user table has initiated properly to the database
def test_database_populate_users(database_engine):
    inspector = inspect(database_engine)
    user_table = inspector.get_table_names()[8]
    columns = inspector.get_columns(user_table)
    column_names = [column['name'] for column in columns]

    with database_engine.connect() as connection:
        select_statement = select(mapper_registry.metadata.tables[user_table])
        result = connection.execute(select_statement)
        all_users = []
        for row in result:
            all_users.append(row[1])
        # file should be empty as no user has been created yet
        assert all_users == []
        # checking if all column are being initiated properly
        assert column_names == ['id', 'username', 'password']

# Test to see if reviews table has initiated properly to the database
def test_database_populate_reviews(database_engine):
    inspector = inspect(database_engine)
    reviews_table = inspector.get_table_names()[7]
    columns = inspector.get_columns(reviews_table)
    column_names = [column['name'] for column in columns]

    with database_engine.connect() as connection:
        select_statement = select(mapper_registry.metadata.tables[reviews_table])
        result = connection.execute(select_statement)
        reviews_table = []
        for row in result:
            reviews_table.append((row[0], row[1], row[2], row[3], row[4]))
        # reviews table content should be empty since there will be no review on startup
        assert reviews_table == []
        # checks if the columns in the review table initiated correctly
        assert column_names == ['id', 'user_id', 'podcast_id', 'rating', 'comment']

# Tests to see if the podcast table populates properly to the database
def test_database_populate_podcast(database_engine):
    inspector = inspect(database_engine)
    podcast_table = inspector.get_table_names()[6]

    columns = inspector.get_columns(podcast_table)
    column_names = [column['name'] for column in columns]
    with database_engine.connect() as connection:
        select_statement = select(mapper_registry.metadata.tables[podcast_table])
        result = connection.execute(select_statement)

        all_podcast = []
        for row in result:
            all_podcast.append((row[0], row[1]))

        num_of_podcast = len(all_podcast)
        assert num_of_podcast == 1001
        assert all_podcast[0] == (1, 'D-Hour Radio Network')
        # checking if all column are being initiated properly
        assert column_names == ['podcast_id', 'title', 'image_url', 'description', 'language', 'website_url', 'author_id', 'itunes_id']

# Tests to see if episodes table populates properly to the database
def test_database_populate_episodes(database_engine):
    inspector = inspect(database_engine)
    episode_table = inspector.get_table_names()[2]

    columns = inspector.get_columns(episode_table)
    column_names = [column['name'] for column in columns]
    with database_engine.connect() as connection:
        select_statement = select(mapper_registry.metadata.tables[episode_table])
        result = connection.execute(select_statement)

        all_episodes = []
        for row in result:
            all_episodes.append((row[1], row[2]))

        num_of_episodes = len(all_episodes)
        assert num_of_episodes == 5634
        assert all_episodes[0] == (14, 'The Mandarian Orange Show Episode 74- Bad Hammer Time, or: 30 Day MoviePass Challenge Part 3')
        # checking if all column are being initiated properly
        assert column_names == ['episode_id', 'podcast_id', 'title', 'audio_url', 'description', 'pub_date']

# Test case to see if author is populating properly to the database
def test_database_populate_author(database_engine):
    inspector = inspect(database_engine)
    author_table = inspector.get_table_names()[0]

    columns = inspector.get_columns(author_table)
    column_names = [column['name'] for column in columns]

    with database_engine.connect() as connection:
        select_statement = select(mapper_registry.metadata.tables[author_table])
        result = connection.execute(select_statement)

        all_author = []
        for row in result:
            all_author.append((row[0], row[1]))

        num_of_author = len(all_author)
        assert num_of_author == 956
        assert all_author[0] == (1, 'D Hour Radio Network')
        # checking if all column are being initiated properly
        assert column_names == ['author_id', 'name']

# Tests to see if playlist is table is populating properly
def test_database_populate_playlist(database_engine):
    inspector = inspect(database_engine)
    playlist_table = inspector.get_table_names()[3]

    columns = inspector.get_columns(playlist_table)
    column_names = [column['name'] for column in columns]

    with database_engine.connect() as connection:
        select_statement = select(mapper_registry.metadata.tables[playlist_table])
        result = connection.execute(select_statement)
        all_playlist = []
        for row in result:
            all_playlist.append(row[0])
        # Empty since there is no playlist to innitiate from the csv files
        assert all_playlist == []
        # checking if all column are being initiated properly
        assert column_names ==  ['playlist_id', 'title', 'owner_id', 'image']

# Test to see if playlist_episodes tables populate properly in the databse
def test_database_populate_playlist_episodes(database_engine):
    inspector = inspect(database_engine)
    playlist_categories_table = inspector.get_table_names()[4]

    columns = inspector.get_columns(playlist_categories_table)
    column_names = [column['name'] for column in columns]

    with database_engine.connect() as connection:
        select_statement = select(mapper_registry.metadata.tables[playlist_categories_table])
        result = connection.execute(select_statement)
        all_playlist_categories = []
        for row in result:
            all_playlist_categories.append(row[0])
        # Empty since there is no playlist to innitiate from the csv files to have a playlist to episode relationship
        assert all_playlist_categories == []
        # checking if all column are being initiated properly
        assert column_names == ['id', 'playlist_id', 'episode_id']

#test to seee if podcast_categories table populates properly to the database
def test_database_populate_podcast_categories(database_engine):
    inspector = inspect(database_engine)
    podcast_categories_table = inspector.get_table_names()[5]

    columns = inspector.get_columns(podcast_categories_table)
    column_names = [column['name'] for column in columns]
    with database_engine.connect() as connection:
        select_statement = select(mapper_registry.metadata.tables[podcast_categories_table]).order_by(
            mapper_registry.metadata.tables[podcast_categories_table].c.podcast_id,
            mapper_registry.metadata.tables[podcast_categories_table].c.category_id
        )
        result = connection.execute(select_statement)

        all_podcast_categories = []
        for row in result:
            all_podcast_categories.append((row[1], row[2]))

        num_of_podcast_categories = len(all_podcast_categories)
        assert num_of_podcast_categories == 2203
        assert all_podcast_categories[0] == (1, 1)
        # checking if all column are being initiated properly
        assert column_names == ['id', 'podcast_id', 'category_id']