from flask import Blueprint, render_template, request

import podcast.adapters.repository as repo
import podcast.podcasts.services as services

podcasts_bp = Blueprint('podcasts_bp', __name__, template_folder='templates')


def filter_podcasts(podcasts, query, parameter):
    searched_podcasts = []
    for podcast in podcasts:
        if parameter == "title" and query in podcast.title:
            searched_podcasts.append(podcast)
        elif parameter == "author" and query in podcast.author.name:
            searched_podcasts.append(podcast)
        elif parameter == "category" and query in podcast.categories[0].name:
            searched_podcasts.append(podcast)

    return searched_podcasts


def calculate_pagination(page, max_pages, list_of_podcasts):
    if page <= 4:
        start = 1
        stop = 8
    else:
        if page + 3 > max_pages:
            stop = max_pages + 1
            start = max_pages - 7
        else:
            start = page - 3
            stop = start + 7
    list_of_podcasts = list_of_podcasts[page * 10 - 10: page * 10]

    return start, stop, list_of_podcasts


def calculate_pages(list_of_podcasts):
    number_of_episodes = len(list_of_podcasts)
    return int(round(number_of_episodes / 10))


@podcasts_bp.route('/podcasts')
def podcasts():
    list_of_podcasts = services.sorted_podcasts_by_title(repo.repository)
    max_pages = calculate_pages(list_of_podcasts)

    if request.args:
        query = request.args.get('q')
        parameter = request.args.get('p')
        page = (request.args.get('page', default=1, type=int))

        if query is not None:
            list_of_podcasts = filter_podcasts(list_of_podcasts, query, parameter)
            max_pages = calculate_pages(list_of_podcasts)

        start, stop, list_of_podcasts = calculate_pagination(page, max_pages, list_of_podcasts)

    else:
        page = 1
        start, stop, list_of_podcasts = calculate_pagination(page, max_pages, list_of_podcasts)

    return render_template('main.html', content_right='podcasts.html', podcasts=list_of_podcasts, start=start,
                           stop=stop, page=page, max_pages=max_pages)
