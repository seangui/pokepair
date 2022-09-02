from dotenv import load_dotenv
import pandas as pd
import numpy as np
import os


def configure():
    load_dotenv()


def get_top_tracks_audio_features_df(spotify):
    user_top_tracks = spotify.current_user_top_tracks(25, 0, 'short_term')
    track_ids = []

    for item in user_top_tracks['items']:
        track_ids = item['id']

    json_of_top_tracks_audio_features = spotify.audio_features(track_ids)
    audio_features_of_top_tracks = {'acousticness': [], 'danceability': [], 'energy': [],
                                    'instrumentalness': [], 'liveness': [], 'loudness': [],
                                    'mode': [], 'speechiness': [], 'tempo': [], 'valence': []}

    for features_of_track in json_of_top_tracks_audio_features:
        audio_features_of_top_tracks['acousticness'].append(features_of_track['acousticness'])
        audio_features_of_top_tracks['danceability'].append(features_of_track['danceability'])
        audio_features_of_top_tracks['energy'].append(features_of_track['energy'])
        audio_features_of_top_tracks['instrumentalness'].append(features_of_track['instrumentalness'])
        audio_features_of_top_tracks['liveness'].append(features_of_track['liveness'])
        audio_features_of_top_tracks['loudness'].append(features_of_track['loudness'])
        audio_features_of_top_tracks['mode'].append(features_of_track['mode'])
        audio_features_of_top_tracks['speechiness'].append(features_of_track['speechiness'])
        audio_features_of_top_tracks['tempo'].append(features_of_track['tempo'])
        audio_features_of_top_tracks['valence'].append(features_of_track['valence'])

    return pd.DataFrame.from_dict(audio_features_of_top_tracks)


def calculate_music_similarity(audio_features_of_top_tracks_df):
    pokemon_names = os.listdir('./app/static/csv_files/')
    pokemon_and_user_similarity_score = {}

    for name_of_pokemon in pokemon_names:
        pokemon_df = pd.read_csv('./app/static/csv_files/' + name_of_pokemon)
        min_distances = []

        for user_audio_features in audio_features_of_top_tracks_df.iterrows():
            user_vector = np.array((user_audio_features[1]['acousticness'], user_audio_features[1]['danceability'],
                                    user_audio_features[1]['energy'], user_audio_features[1]['instrumentalness'],
                                    user_audio_features[1]['liveness'], user_audio_features[1]['loudness'],
                                    user_audio_features[1]['mode'], user_audio_features[1]['speechiness'],
                                    user_audio_features[1]['tempo'], user_audio_features[1]['valence']))

            min_dist = float('inf')

            for pokemon_audio_features in pokemon_df.iterrows():
                pokemon_vector = np.array((pokemon_audio_features[1]['acousticness'], pokemon_audio_features[1]['danceability'],
                                           pokemon_audio_features[1]['energy'], pokemon_audio_features[1]['instrumentalness'],
                                           pokemon_audio_features[1]['liveness'], pokemon_audio_features[1]['loudness'],
                                           pokemon_audio_features[1]['mode'], pokemon_audio_features[1]['speechiness'],
                                           pokemon_audio_features[1]['tempo'], pokemon_audio_features[1]['valence']))

                distance = np.linalg.norm(user_vector - pokemon_vector)

                if distance < min_dist:
                    min_dist = distance

            min_distances.append(min_dist)

        average_of_min_dist = np.mean(min_distances)
        pokemon_and_user_similarity_score[name_of_pokemon.split('.csv')[0]] = average_of_min_dist

    # return "oshawott"
    return min(pokemon_and_user_similarity_score, key=pokemon_and_user_similarity_score.get)


def create_pokemon_information():
    pokemon_information = {}

    pokemon_information['chikorita'] = PokemonInformation("#6ab429", "Matthew Chun",
                                                          "Chikorita is a baddie She whips her leaf like she'll whoop you with her vine whip")

    pokemon_information['cyndaquil'] = PokemonInformation("#ff5a00", "Alexis Rosas",
                                                          "So cyndaquill is a broken hearted woman, a little depressed, in her early 20s and on the "
                                                          "road to self discovery. She prioritizes herself and her well being but is going through a "
                                                          "rough patch in her relationship with herself and this is reflected in her music.")

    pokemon_information['totodile'] = PokemonInformation("#315a83", "Emmi Umbach",
                                                         "Totodile is a super joyous Pokemon that enjoys having fun and can be a bit rambunctious when they want to. They also are a bit of a lover and tend to fall easily for someone")

    pokemon_information['mudkip'] = PokemonInformation("#41a4de", "Raymond Constancio",
                                                         "Mudkip listens to Yeat")

    pokemon_information['fennekin'] = PokemonInformation("#e35a36", "Daniel Velez",
                                                         "Fennekin is a very friendly and kind-hearted Pokemon with a very bold heart. Her playlist is relaxing, chill, and confidence-boosting. Fennekin is a cute pokemon who likes to stay clean, making her a bit of a primadonna but don't let that fool you as she will fight if it's for a good cause")

    pokemon_information['popplio'] = PokemonInformation("#4e76ba", "Mary Esguerra",
                                                         "Popplio is a little naive and sees the world through rose-colored glasses. He is in his late teens and is about to enter college majoring in something artsy, not knowing that it won’t pay him well when he’s 25. But for now, he’s having summer fun with his closest friend by playing in beaches and throwing pool parties.")

    pokemon_information['oshawott'] = PokemonInformation("#57a2af", "Lisa Cooley",
                                                         "Oshawott loves upbeat pop, reggare-rock and Disney singalong to soulful, lyrica rap r*b and indie tracks. Oshawott would like the messages about having fun, appreciating life and being yourself swimming upside down :)")

    pokemon_information['scorbunny'] = PokemonInformation("#ce6d51", "Jeadelle Gustave",
                                                          "Hoppity hop hop. It's scorbunnies playlist full of hip hopity hop. He's a fire type so you know it's lit. Just like you.")

    pokemon_information['tepig'] = PokemonInformation("#ed9555", "Gary Hu",
                                                          "when he looks like: ❤️✨☺️ but actually is like: ☠️⛓🖤")

    return pokemon_information


class PokemonInformation:
    def __init__(self, color, playlist_creator_name, description):
        self.color = color
        self.playlist_creator_name = playlist_creator_name
        self.description = description
