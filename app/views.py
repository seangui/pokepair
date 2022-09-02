from flask import Blueprint, request, redirect, render_template, session
import os
import uuid
import spotipy
from app import pokify_util

views = Blueprint('views', __name__)


os.environ["SPOTIPY_CLIENT_ID"] = '#'
os.environ["SPOTIPY_CLIENT_SECRET"] = '#'
os.environ["SPOTIPY_REDIRECT_URI"] = 'http://127.0.0.1:5000/'

caches_folder = './.spotify_caches/'
if not os.path.exists(caches_folder):
    os.makedirs(caches_folder)


def session_cache_path():
    return caches_folder + session.get('uuid')


@views.route('/')
def home():
    if not session.get('uuid'):
        # Step 1. giving random id to unknown visitors
        session['uuid'] = str(uuid.uuid4())

    cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=session_cache_path())
    auth_manager = spotipy.oauth2.SpotifyOAuth(scope='user-top-read',
                                               cache_handler=cache_handler,
                                               show_dialog=True)

    if request.args.get("code"):
        # Step 3. Being redirected from Spotify auth page
        auth_manager.get_access_token(request.args.get("code"))
        return redirect('/result')

    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        # Step 2. Display sign in link when no token
        auth_url = auth_manager.get_authorize_url()
        return render_template("home.html", theme_color="#c5294e", url=auth_url)

    # Step 4. Signed in, display data
    return render_template("home.html", theme_color="#c5294e", url="/result")


@views.route('/result')
def result():
    cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=session_cache_path())
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)

    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/')

    spotify = spotipy.Spotify(auth_manager=auth_manager)

    audio_features_of_top_tracks_df = pokify_util.get_top_tracks_audio_features_df(spotify)
    most_similar_pokemon = pokify_util.calculate_music_similarity(audio_features_of_top_tracks_df)

    pokemon_information = pokify_util.create_pokemon_information()

    # pokemon_colors = {"bulbasaur": "#73ac31", "charmander": "#de5138", "squirtle": "#6390f0",
    #                   "chikorita": "#6ab429", "cyndaquil": "#ff5a00", "totodile": "#315a83",
    #                   "treecko": "#acde6a", "torchic": "#ff8b31", "mudkip": "#41a4de",
    #                   "turtwig": "#39a441", "chimchar": "#cc792b", "piplup": "#4382b7",
    #                   "snivy": "#088300", "tepig": "#ed9555", "oshawott": "#57a2af",
    #                   "chespin": "#849f4e", "fennekin": "#e35a36", "froakie": "#58c0ea",
    #                   "rowlet": "#25ac89", "litten": "#ea5b48", "popplio": "#4e76ba",
    #                   "grookey": "#2b8854", "scorbunny": "#ce6d51", "sobble": "#274eab"}

    image = "/static/images/pokemon/" + most_similar_pokemon + ".webp"
    color = pokemon_information[most_similar_pokemon].color
    return render_template("result.html", theme_color=color, image_source=image,
                           pokemon_name=most_similar_pokemon.capitalize(),
                           playlist_creator_name=pokemon_information[most_similar_pokemon].playlist_creator_name,
                           description=pokemon_information[most_similar_pokemon].description)



