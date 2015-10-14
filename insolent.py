import flask
import json
import functools
import logging
logging.basicConfig(level=logging.INFO)

app = flask.Flask(__name__)

@app.before_request
def before_request(*args, **kwargs):
    log_result = dict()
    log_result['request'] = dict(headers=list(flask.request.headers), url=flask.request.url, method=flask.request.method, cookies=flask.request.cookies)
    log_result['request']['body'] = flask.request.get_json(force=True,silent=True) or flask.request.data

    app.logger.info(json.dumps(log_result, sort_keys=True))


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    if len(flask.request.url) < 7:
        app.logger.info("URL too small: {0}".format(flask.request.url))
        return flask.Request(status_code=400)

    if 'http:' == flask.request.url[0:5].lower():
        app.logger.info("Redirecting to https:" + flask.request.url[5:])
        return flask.redirect('https:' + flask.request.url[5:]),301

    app.logger.info("URL is already https possibly...")
    return flask.Request("Hi", status_code=500)

if __name__ == "__main__":
    app.run('0.0.0.0', port=8080)
