import os
import urllib.request
import urllib.parse
import time


def _get_input_file_name(day):
    input_dir = "{}/input".format(os.getcwd())
    if not os.path.exists(input_dir):
        os.makedirs(input_dir)
    input_file = "{}/day_{}".format(input_dir, day)
    return input_file


def _check_input_file(day):
    input_file = _get_input_file_name(day)
    if os.path.exists(input_file):
        f = open(input_file, "r")
        print("Reusing data from {}".format(input_file))
        return f.read()
    return None


def fetch(year, day):
    cached = _check_input_file(day)
    if cached:
        return cached

    sid = os.environ.get('aoc_sessionid')

    url = 'https://adventofcode.com/{}/day/{}/input'.format(year, day)

    headers = {'cookie': 'session={}'.format(sid)}

    data = urllib.parse.urlencode({})
    data = data.encode('ascii')
    req = urllib.request.Request(url, data, headers)
    with urllib.request.urlopen(req) as response:
        resp = response.read().decode('utf-8').strip()
    f = open(_get_input_file_name(day), "w")
    f.write(resp)
    f.close()
    return resp


def time_it(l, *args):
    t = time.process_time_ns()
    r = l(*args)
    t = (time.process_time_ns() - t) / 1000 / 1000
    return r, t
