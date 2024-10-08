from sqlalchemy import select, inspect

from podcast.adapters.orm import mapper_registry

# Test case to see if the tables name are bieng populated properly
def test_database_populate_inspect_table_names(database_engine):
    # Get table information
    inspector = inspect(database_engine)
    assert inspector.get_table_names() == ['authors', 'categories', 'episodes', 'playlist', 'playlist_episodes',
                                           'podcast_categories', 'podcasts', 'reviews', 'users']

# Test case to see if the categories is being populated correctly
def test_database_populate_categories(database_engine):
        inspector = inspect(database_engine)
        categories = inspector.get_table_names()[1]

        with database_engine.connect() as connection:
            select_statement = select(mapper_registry.metadata.tables[categories])
            result = connection.execute(select_statement)

            categories_name = []
            for row in result:
                categories_name.append(row[1])

            assert categories_name[0:4] == ['Society & Culture', 'Personal Journals', 'Professional', 'News & Politics']