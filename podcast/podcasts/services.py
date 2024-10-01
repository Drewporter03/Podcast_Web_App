from podcast.adapters.repository import AbstractRepository


def get_episodes(repo: AbstractRepository):
    """list_of_episodes = []
    for i in range(1, repo.get_number_of_episodes() + 1):
        episode = repo.get_episode(i)
        list_of_episodes.append(episode)
    return list_of_episodes"""
    # NEED TO REMOVE - CAN JUST CALL FROM BP
    return repo.get_episodes()


def get_podcasts(repo: AbstractRepository):
    return repo.get_podcasts()



def sorted_podcasts_by_title(repo: AbstractRepository):
    list_of_podcasts = get_podcasts(repo)
    return sorted(list_of_podcasts, key=lambda podcast: podcast.title)


def filter_podcasts(podcasts, query, parameter):
    searched_podcasts = []
    for podcast in podcasts:
        if parameter == "title" and query.lower() in podcast.title.lower():
            searched_podcasts.append(podcast)
        elif parameter == "author" and query.lower() in podcast.author.name.lower():
            searched_podcasts.append(podcast)
        elif parameter == "category" and query.lower() in podcast.categories[0].name.lower():
            searched_podcasts.append(podcast)

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
