import os

from flask import Flask, jsonify, request
from flask_cors import CORS
from supabase import create_client, Client


app = Flask(__name__)

CORS(
    app,
    resources={
        r"/api/*": {
            "origins": "*"
        }
    }
)


SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")


if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError(
        "Не заданы SUPABASE_URL и SUPABASE_KEY"
    )


supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)


ANIME_TABLE = "Anime sait"
EPISODES_TABLE = "episodes"


@app.route("/")
def home():

    return jsonify({
        "status": "ok",
        "message": "Mirai Anime API работает!"
    })


@app.route("/api/health")
def health():

    return jsonify({
        "status": "ok"
    })


@app.route("/api/anime")
def get_anime():

    try:

        response = (
            supabase
            .table(ANIME_TABLE)
            .select("*")
            .order(
                "created_at",
                desc=True
            )
            .execute()
        )

        data = response.data or []

        anime_list = []

        for anime in data:

            anime_list.append({
                "id": anime.get("id"),
                "title": anime.get(
                    "title",
                    "Без названия"
                ),
                "year": anime.get(
                    "year",
                    0
                ),
                "episodes": anime.get(
                    "episodes",
                    0
                ),
                "rating": anime.get(
                    "rating",
                    0
                ),
                "genres": anime.get(
                    "genres",
                    []
                ),
                "description": anime.get(
                    "description",
                    ""
                ),
                "poster": anime.get(
                    "poster",
                    ""
                ),
                "popular": anime.get(
                    "popular",
                    False
                )
            })

        return jsonify({
            "anime": anime_list
        })

    except Exception as e:

        print(
            "ANIME ERROR:",
            repr(e)
        )

        return jsonify({
            "error": str(e)
        }), 500


@app.route("/api/episodes")
def get_episodes():

    anime_id = request.args.get(
        "anime_id"
    )

    if not anime_id:

        return jsonify({
            "error":
                "Не указан anime_id"
        }), 400

    try:

        response = (
            supabase
            .table(EPISODES_TABLE)
            .select("*")
            .eq(
                "anime_id",
                anime_id
            )
            .order(
                "season",
                desc=False
            )
            .order(
                "episode",
                desc=False
            )
            .execute()
        )

        episodes = response.data or []

        result = []

        for item in episodes:

            result.append({
                "id": item.get("id"),
                "anime_id": item.get("anime_id"),
                "season": item.get(
                    "season",
                    1
                ),
                "episode": item.get(
                    "episode",
                    1
                ),
                "dub": item.get(
                    "dub",
                    ""
                ),
                "quality": item.get(
                    "quality",
                    ""
                ),
                "video_url": item.get(
                    "video_url",
                    ""
                )
            })

        return jsonify({
            "episodes": result
        })

    except Exception as e:

        print(
            "EPISODES ERROR:",
            repr(e)
        )

        return jsonify({
            "error": str(e)
        }), 500


@app.route("/api/episode")
def get_episode():

    anime_id = request.args.get(
        "anime_id"
    )

    season = request.args.get(
        "season",
        "1"
    )

    episode = request.args.get(
        "episode"
    )

    if not anime_id:

        return jsonify({
            "error":
                "Не указан anime_id"
        }), 400

    if not episode:

        return jsonify({
            "error":
                "Не указан episode"
        }), 400

    try:

        response = (
            supabase
            .table(EPISODES_TABLE)
            .select("*")
            .eq(
                "anime_id",
                anime_id
            )
            .eq(
                "season",
                int(season)
            )
            .eq(
                "episode",
                int(episode)
            )
            .order(
                "quality",
                desc=False
            )
            .execute()
        )

        episodes = response.data or []

        result = []

        for item in episodes:

            result.append({
                "id": item.get("id"),
                "anime_id": item.get("anime_id"),
                "season": item.get(
                    "season",
                    1
                ),
                "episode": item.get(
                    "episode",
                    1
                ),
                "dub": item.get(
                    "dub",
                    ""
                ),
                "quality": item.get(
                    "quality",
                    ""
                ),
                "video_url": item.get(
                    "video_url",
                    ""
                )
            })

        return jsonify({
            "episodes": result
        })

    except Exception as e:

        print(
            "EPISODE ERROR:",
            repr(e)
        )

        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":

    port = int(
        os.environ.get(
            "PORT",
            5000
        )
    )

    app.run(
        host="0.0.0.0",
        port=port
  )
