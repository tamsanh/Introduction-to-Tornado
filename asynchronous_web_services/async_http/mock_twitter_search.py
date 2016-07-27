import json
import datetime
from random import randint

import tornado.web
import tornado.httpserver
import tornado.httpclient
import tornado.ioloop

"""
{
    "results": [
        {"createdAt": "%a, %d %b %Y %H:%M:%S +0000"}
    ]
}
"""


def mock_tweet(number_minutes_ago):
    dt = datetime.datetime.now() - datetime.timedelta(minutes=number_minutes_ago)
    return {"created_at": dt.strftime("%a, %d %b %Y %H:%M:%S +0000")}


class FakeTweetHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        super(FakeTweetHandler, self).data_received(chunk)

    def get(self):
        num_of_tweets = randint(0, 50000)
        mock_tweets_list = []
        for _ in range(num_of_tweets):
            random_minutes_ago = randint(0, 10)
            mock_tweets_list.append(mock_tweet(random_minutes_ago))
        mock_tweets_list = sorted(mock_tweets_list, key=lambda x: x["created_at"], reverse=True)
        ret = {"results": mock_tweets_list}
        self.write(json.dumps(ret, indent=4))


if __name__ == "__main__":
    app = tornado.web.Application(handlers=[(r"/", FakeTweetHandler)])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(9999)
    tornado.ioloop.IOLoop.instance().start()
