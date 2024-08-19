from flask import Blueprint, render_template, request
import podcast.episodes.services as services
import podcast.adapters.repository as repo
from podcast.episodes.services import get_podcasts, get_episodes

episodes_bp = Blueprint('episode_bp', __name__, template_folder='templates')


@episodes_bp.route('/episodes')
def episodes():
    list_of_podcasts = get_podcasts(repo.repository)

    podcast_id = request.args.get('podcast_id', default=1, type=int)

    podcast = list_of_podcasts[podcast_id]

    if request.args.get('page'):
        page = int(request.args.get('page'))
        list_of_episodes = get_episodes(repo.repository, podcast_id)[:6]
        if page <= 4:
            start = 1
            stop = 8
        else:
            start = page - 3
            stop = page + 3
    else:
        list_of_episodes = get_episodes(repo.repository, podcast_id)[1:7]
        print(list_of_episodes)
        print(list_of_episodes[0].podcast_id == podcast.id)
        start, stop = 1, 8    


    return render_template('main.html', content_right='episodes.html', podcast=podcast, episodes=list_of_episodes)
