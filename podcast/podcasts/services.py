from podcast.adapters.repository import AbstractRepository


def get_episodes(repo: AbstractRepository):
    return repo.get_episodes()


def get_podcasts(repo: AbstractRepository):
    return repo.get_podcasts()


def sorted_podcasts_by_title(repo: AbstractRepository):
    list_of_podcasts = get_podcasts(repo)
    return sorted(list_of_podcasts, key=lambda podcast: podcast.title)


def filter_podcasts(query, parameter, repo: AbstractRepository):
    if parameter == "title":
        searched_podcasts = repo.search_podcast_by_title(query)
    elif parameter == "author":
        searched_podcasts = repo.search_podcast_by_author(query)
    elif parameter == "category":
        query = query.strip()
        searched_podcasts = repo.search_podcast_by_category(query)
    else:
        searched_podcasts = repo.search_podcast_by_title(query)
    return searched_podcasts


def calculate_pagination(page, max_pages, list_of_podcasts):
    if page <= 4:
        start = 1
        stop = 8 if max_pages > 8 else max_pages + 1
    else:
        if page + 3 > max_pages:
            stop = max_pages + 1
            start = 1 if max_pages - 7 <= 1 else max_pages - 7
        else:
            start = page - 3
            stop = start + 7
    list_of_podcasts = list_of_podcasts[page * 10 - 10: page * 10]

    return start, stop, list_of_podcasts


def calculate_pages(list_of_podcasts):
    number_of_episodes = len(list_of_podcasts)
    return int(round(number_of_episodes / 10))


def get_user(repo: AbstractRepository, user_name: str):
    user = repo.get_user(user_name)
    return user
