import config
from model import Vote,Voter
from sqlalchemy import func,desc
db = config.db

import vote_bo
import vote_dao
import voter_dao
import option_dao
import hashlib


def randomized_list(v,options_array):
    counting = vote_dao.counts_votes_by_votation(v.votation_id) # a dict of dicts
    i = 0
    d = {}
    counting_keys = list(counting.keys())
    counting_keys.sort()
    for option_id in counting_keys:
        option_count = counting[option_id] # a dict
        s = str(i+1) + " "
        options_keys = list(option_count.keys())
        options_keys.sort()
        comma = ''
        for jud_id in options_keys:
            s += comma + str(option_count[jud_id])
            comma = ',' 
        h = hashlib.sha256()
        h.update(s.encode())
        d[h.hexdigest()] = (s,options_array[i].option_name) 
        i += 1
    # sorting by hash:
    ar = []
    d_keys = list(d.keys())
    d_keys.sort()
    for h in d_keys:
        ar.append((d[h][1],d[h][0],h))
    return ar


