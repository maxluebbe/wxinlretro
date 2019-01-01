#!/usr/bin/python3

import functools
import hashlib
import os
import pickle
import sys

from common import Game

@functools.lru_cache()
def _load_game_dict(game_dict_filename):
    games_by_sha1 = None
    with open(game_dict_filename, 'rb') as f:
        games_by_sha1 = pickle.loads(f.read())
        f.close()
    return games_by_sha1


def _compute_sha1_hexdigest(filename):
    sha1 = hashlib.sha1()
    with open(filename, 'rb') as f:
        while True:
            data = f.read(1024)
            if not data:
                break
            sha1.update(data)
    return sha1.hexdigest().upper()


def _match_game(filename):
    games_dict = _load_game_dict(os.path.join('data', 'genesis.p'))
    games_dict.update(_load_game_dict(os.path.join('data', 'n64.p')))
    games_dict.update(_load_game_dict(os.path.join('data', 'gba.p')))
    games_dict.update(_load_game_dict(os.path.join('data', 'nes_headerless.p')))
    d = _compute_sha1_hexdigest(filename)
    g = None
    if d in games_dict:
        g = games_dict[d]
    return g


def identify(filenames):    
    for f in filenames:
        # Check if is file before trying to match.
        if os.path.isfile(f):
            g = _match_game(f)
            if g:
                print("\"%s\" appears to be: \"%s\"" % (f, g.filename))
            else:
                print('\"%s\" does not look like any known rom...' % f)


def rename(filenames):
    for f in filenames:
        if os.path.isfile(f):
            g = _match_game(f)
            if g:
                print("\"%s\" appears to be: \"%s\", renaming!" % (f, g.filename))
                os.rename(f, os.path.join(os.path.dirname(f), g.filename))


def display_usage(script_name):
    print('Usage:')
    print('$ python3 %s identify [filenames]' % script_name)
    print('$ python3 %s rename [filenames]' % script_name)


def main(argv):
    if len(argv) < 3:
        display_usage(argv[0])
        return 1
    if argv[1] == 'identify':
        identify(argv[2:])
    elif argv[1] == 'rename':
        rename(argv[2:])


if __name__ == '__main__':
    main(sys.argv)