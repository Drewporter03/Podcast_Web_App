from flask import Blueprint, render_template, request

import podcast
from podcast.adapters.datareader.csvdatareader import CSVDataReader
import podcast.podcasts.services as services
import podcast.adapters.repository as repo
from podcast.adapters.memory_repository import MemoryRepository, populate
from podcast.adapters.repository import AbstractRepository




podcasts_bp = Blueprint('podcasts_bp', __name__, template_folder='templates')


@podcasts_bp.route('/podcasts')
def podcasts():

    number_of_episodes = len(services.get_podcasts(repo.repository))
    max_pages = int(round(number_of_episodes/10))

    if request.args:
        query = request.args.get('q')
        parameter = request.args.get('p')
        page = int(request.args.get('page', default=1, type=int))
        list_of_podcasts = services.sorted_podcasts_by_title(repo.repository)[page * 10 - 10: page * 10]
        if query is not None:
            filtered_list_of_podcasts = []
            if parameter == "title":
                for podcast in list_of_podcasts:
                    if query in podcast.title:
                        filtered_list_of_podcasts.append(podcast)
            if parameter == "author":
                for podcast in list_of_podcasts:
                    if query in podcast.author.name:
                        filtered_list_of_podcasts.append(podcast)
            if parameter == "category":
                for podcast in list_of_podcasts:
                    if query in podcast.categories:
                        filtered_list_of_podcasts.append(podcast)
            list_of_podcasts = filtered_list_of_podcasts
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

    return render_template('main.html', content_right='podcasts.html', podcasts=list_of_podcasts, start = start, stop = stop, page=page, max_pages = max_pages)
