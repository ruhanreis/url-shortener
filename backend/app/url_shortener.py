from flask import Flask, request, jsonify
from werkzeug.exceptions import HTTPException
from random import randint
import redis
import operator

app = Flask(__name__)
r = redis.Redis( host='redis', port=6379 )

valid_chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

SHORT_URL_HOST=""
USERS_KEY="users"
USER_URLS_KEY="users:urls:"
URLS_KEY="urls:"

ID_FIELD="id"
USER_ID="user_id"
HITS_FIELD="hits"
URL_FIELD="url"
SHORT_URL_FIELD="short_url"

@app.route('/urls/<id>', methods=['GET'])
def get_urls(id):
    if not r.exists(URLS_KEY + id):
        return "", 404

    url = r.hmget(URLS_KEY + id, URL_FIELD)
    r.hincrby(URLS_KEY + id, HITS_FIELD, 1)

    return url[0], 301


@app.route('/users/<userid>/urls', methods=['POST'])
def post_user_url(userid):

    try:
        url = request.json['url']

        if not (r.sismember(USERS_KEY, userid)):
            return jsonify(error="O id de usuario " + userid + " nao existe"), 404

        random_url_id = shorten(url)

        r.sadd(USER_URLS_KEY + userid, random_url_id)

        url_dict = {
                ID_FIELD:random_url_id
            ,   USER_ID:userid
            ,   HITS_FIELD:0
            ,   URL_FIELD: url
            ,   SHORT_URL_FIELD: request.host_url + random_url_id
        }

        r.hmset(URLS_KEY + random_url_id, url_dict)

        del url_dict[USER_ID]
        url_dict_response = url_dict

    except KeyError as e:
        return "A url nao pode ser vazia", 400


    return jsonify(url_dict_response), 201


@app.route('/stats', methods=['GET'])
def get_stats():
    users = r.smembers(USERS_KEY)

    total_hits = 0
    all_urls = []

    for user in users:
        urls = r.smembers(USER_URLS_KEY + user)

        for url in urls:
            stats = getStats(url)

            all_urls.append(stats)
            total_hits += stats[HITS_FIELD]

    total_urls = len(all_urls)
    all_urls.sort(key=operator.itemgetter(HITS_FIELD), reverse=True)

    top_ten_hits = all_urls[:10]

    stats_dict = {
            "hits": total_hits
        ,   "urlCount": total_urls
        ,   "topUrls": top_ten_hits
    }

    return jsonify(stats_dict), 200


@app.route('/users/<userid>/stats', methods=['GET'])
def get_user_stats(userid):
    if not r.sismember(USERS_KEY, userid):
        return "", 404

    urls = r.smembers(USER_URLS_KEY + userid)

    total_hits = 0
    all_urls = []

    for url in urls:
        stats = getStats(url)

        all_urls.append( stats )
        total_hits += stats[HITS_FIELD]

    total_urls = len( all_urls )
    all_urls.sort(key = operator.itemgetter(HITS_FIELD), reverse = True)

    top_ten_hits = all_urls[:10]

    stats_dict = {
            "hits": total_hits
        ,   "urlCount": total_urls
        ,   "topUrls": top_ten_hits
    }

    return jsonify(stats_dict), 200


@app.route('/stats/<id>', methods=['GET'])
def get_url_stats(id):
    if not r.exists(URLS_KEY + id):
        return "", 404

    stats = getStats(id)
    return jsonify(stats), 200


@app.route('/urls/<id>', methods=['DELETE'])
def delete_url(id):
    if not r.exists(URLS_KEY + id):
        return "", 404

    info = r.hgetall(URLS_KEY + id)
    userid = info[USER_ID]

    r.srem(USER_URLS_KEY + userid, id)
    r.delete(URLS_KEY + id)

    return "", 200


@app.route('/users', methods=['POST'])
def post_user():

    try:
        userid = request.json['id']

        if r.sismember("users", userid):
            return jsonify(error="O id passado ja existe"), 409

        r.sadd("users", userid)

    except KeyError as e:
        return jsonify(error="O id nao pode ser vazio"), 400

    return jsonify(request.json), 201


@app.route('/user/<userid>', methods=['DELETE'])
def delete_user(userid):
    if not r.sismember(USERS_KEY, userid):
        return "", 404

    urls = r.smembers(USER_URLS_KEY + userid)

    for url in urls:
        r.delete(URLS_KEY + url)

    r.delete(USER_URLS_KEY + userid)
    r.srem(USERS_KEY, id)

    return "", 200

@app.errorhandler(Exception)
def handle_error(e):
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    return jsonify(error="Ocorreu um erro inesperado"), code

def getStats(url):
    stats = r.hgetall(URLS_KEY + url)

    hits = stats[HITS_FIELD]
    stats[HITS_FIELD] = int(hits)

    del stats[USER_ID]

    return stats


def shorten(long_url, n=6):
    short_id = ""
    for i in range(n):
        short_id += valid_chars[randint(0,len(valid_chars)-1)]
    return short_id


if __name__ == '__main__':
    app.run(host='0.0.0.0')



