from flask import Blueprint, render_template, request
import podcast.episodes.services as services
import podcast.adapters.repository as repo


episodes_bp = Blueprint('episode_bp', __name__, template_folder='templates')


@episodes_bp.route('/episodes')
def episodes():
    if request.args:
        podcast_id = (request.args.get('podcast_id'))
    list_of_podcasts = services.get_podcasts(repo.repository)
    return render_template('main.html', content_right='episodes.html', podcast=podcast_id, podcasts=list_of_podcasts)
