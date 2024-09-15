from flask import Blueprint, render_template, request
import podcast.episodes.services as services
import podcast.adapters.repository as repo
from podcast.episodes.services import get_podcasts, get_episodes

episodes_bp = Blueprint('episode_bp', __name__, template_folder='templates')


@episodes_bp.route('/episodes')
def episodes():
    """TEST REVIEW"""
    services.add_review(7, "good", 4, "bob", repo.repository)
    services.add_review(7, "bad", 2, "john", repo.repository)

    list_of_podcasts = get_podcasts(repo.repository)

    podcast_id = request.args.get('podcast_id', type=int)
    list_of_episodes = services.sorted_episodes_by_date(repo.repository, podcast_id)
    average = services.get_average_reviews(podcast_id, repo.repository)
    reviews = services.get_podcast_reviews(podcast_id, repo.repository)

    count = 0
    for episode in list_of_episodes:
        if episode.podcast_id == podcast_id:
            count += 1

    max_pages = (count // 10)

    podcast = list_of_podcasts[podcast_id]

    if request.args.get('page'):
        page = int(request.args.get('page'))
        list_of_episodes = services.sorted_episodes_by_date(repo.repository, podcast_id)[page * 10 - 10: page * 10]
        if page <= 4:
            start = 1
            stop = 8 if max_pages > 8 else max_pages + 1
        else:
            if page + 3 > max_pages:
                stop = max_pages + 1
                start = max_pages - 7
            else:
                start = page - 3
                stop = start + 7
    else:
        list_of_episodes = services.sorted_episodes_by_date(repo.repository, podcast_id)[:10]
        start = 1
        stop = max_pages + 1 if start + 8 > max_pages else start + 7
        page = 1

    return render_template('main.html', content_right='episodes.html', podcast=podcast, podcast_id=podcast_id,
                           episodes=list_of_episodes, start=start, stop=stop, page=page, max_page=max_pages,
                           reviews=reviews, average = average)

