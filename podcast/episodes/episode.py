from flask import Blueprint, render_template, request
import podcast.episodes.services as services
import podcast.adapters.repository as repo
from podcast.episodes.services import get_podcasts, get_episodes

episodes_bp = Blueprint('episode_bp', __name__, template_folder='templates')


@episodes_bp.route('/episodes')
def episodes():
    list_of_podcasts = get_podcasts(repo.repository)

    podcast_id = request.args.get('podcast_id', type=int)
    print(request.args)
    podcast = list_of_podcasts[podcast_id]

    if request.args.get('page'):
        page = int(request.args.get('page'))
        list_of_episodes = get_episodes(repo.repository, podcast_id)[page * 6 - 6: page * 6]
        if page <= 4:
            start = 1
            stop = 8
        else:
            start = page - 3
            stop = page + 4 if page + 3 < 167 else 168
    else:
        list_of_episodes = get_episodes(repo.repository, podcast_id)[:6]
        start, stop = 1, 8
        page = 1


    return render_template('main.html', content_right='episodes.html', podcast=podcast, podcast_id = podcast_id, episodes=list_of_episodes, start = start, stop = stop, page=page)
