#import hashlib
import os.path
import subprocess as sp
import config
import vote

HEXSTRING_LEN_GUAR = 55
HEXSTRING_LEN_CAND = 48

MOCK = True
#MOCK = False

def string2hex(key, key_length):
    if key == None:
        return None
    s = key.ljust(key_length)
    result = ''
    for c in s:
        result = "%s%0.2X" % (result, ord(c))
    return result

def hash_string(s):
    cp1 = sp.run([os.path.join(config.BINPATH,"Hash"), s], stdout=sp.PIPE)
    return cp1.stdout[15:-2]

def election_dir(votation_id):
    election_dir = os.path.join(config.ELECTIONPATH, "election_majority{}".format(votation_id))
    return election_dir


def create_election(votation_id, candidates_n,words_n):
    """Backend program Creation"""
    if MOCK: return True
    cp = sp.run([os.path.join(config.BINPATH, "Creation"), election_dir(votation_id), str(candidates_n), str(words_n)], stdout=sp.PIPE)
    control_string = "Election successfully created with {} candidates and {} words".format(candidates_n, words_n)
    if cp.stdout.decode('utf-8').startswith(control_string):
        return True
    else:
        return False

def election_state(votation_id):
    if MOCK: return ["Lorem ipsum dolor sit amet, consectetur adipiscing elit,","sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.","Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat."]
    p1 = election_dir(votation_id)
    cp = sp.run([os.path.join(config.BINPATH, "State"), p1], stdout=sp.PIPE)
    s =  cp.stdout.decode('utf-8')
    ar = s.split('\n')
    return ar

def election_pipe_in(votation_id):
    election_pipe = os.path.join(config.ELECTIONPATH, "election_majority_in{}".format(votation_id))
    return election_pipe

def election_pipe_out(votation_id):
    election_pipe = os.path.join(config.ELECTIONPATH, "election_majority_out{}".format(votation_id))
    return election_pipe

def election_vote_sec(votation_id, vote_array):
    # read from a named pipe
    result = None
    pipe_in =  open(election_pipe_in(votation_id),"w") # write votes here
    pipe_out = open(election_pipe_out(votation_id),"r") # read results from here
    vote_line = str(user_id)
    successful_message = "{} OK".format(user_id)
    for n in vote_array:
        vote_line = ("{} {}".format(vote_line,n))
    print(vote_line, file=pipe_in)
    vote_result = pipe_out.readline()
    pipe_in.close()
    pipe_out.close()
    if MOCK:
        result = True
    else:
        result = vote_result == successful_message
    return result

