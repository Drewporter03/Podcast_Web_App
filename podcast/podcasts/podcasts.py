from flask import Blueprint, render_template, request

import podcast
from podcast.adapters.datareader.csvdatareader import CSVDataReader
import podcast.podcasts.services as services
import podcast.adapters.repository as repo
from podcast.adapters.memory_repository import MemoryRepository, populate
from podcast.adapters.repository import AbstractRepository

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


@podcasts_bp.route('/podcasts')
def podcasts():
    number_of_episodes = len(services.get_podcasts(repo.repository))
    max_pages = int(round(number_of_episodes / 10))

    if request.args:
        query = request.args.get('q')
        parameter = request.args.get('p')
        page = int(request.args.get('page', default=1, type=int))
        list_of_podcasts = services.sorted_podcasts_by_title(repo.repository)[page * 10 - 10: page * 10]
        if query is not None:
            list_of_podcasts = filter_podcasts(services.sorted_podcasts_by_title(repo.repository), query, parameter)
            number_of_episodes = len(list_of_podcasts)
            max_pages = (round(number_of_episodes / 10))
            list_of_podcasts = list_of_podcasts[page * 10 - 10: page * 10]


        if page <= 4:
            start = 1
            stop = 8
        else:
            start = page - 3
            stop = page + 4 if page + 3 < max_pages else max_pages + 1
            if page + 3 > max_pages:
                stop = max_pages + 1
                start = max_pages - 7
            else:
                start = page - 3
                stop = start + 7
    else:
        list_of_podcasts = services.sorted_podcasts_by_title(repo.repository)[:10]
        start, stop = 1, 8
        page = 1

    return render_template('main.html', content_right='podcasts.html', podcasts=list_of_podcasts, start=start,
                           stop=stop, page=page, max_pages=max_pages)
