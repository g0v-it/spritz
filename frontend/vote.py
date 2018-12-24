import dbmanager
import config
import option
import voter
import votation

class vote_dto:
    """DTO class for the database table"""
    def __init__(self):
        self.vote_key = None
        self.votation_id = None
        self.option_id = None
        self.jud_value = None


def insert_dto(o):
    conn = dbmanager.get_connection()
    c = conn.cursor()
    c.execute("""insert into vote(
                    vote_key, votation_id, option_id,jud_value) values (%s,%s,%s,%s)""",(o.vote_key,o.votation_id, o.option_id ,o.jud_value) )
    c.close()
    conn.close()

def delete_votes_by_key(vote_key):
    conn = dbmanager.get_connection()
    c = conn.cursor()
    c.execute("delete from vote where vote_key = %s", (vote_key,) )
    c.close()
    conn.close()

def delete_votes_by_votation_id(votation_id):
    """
    For testing pourpose
    """
    conn = dbmanager.get_connection()
    c = conn.cursor()
    c.execute("delete from vote where votation_id = %s", (votation_id,) )
    c.close()
    conn.close()


def save_votes(user_id, vote_key,votation_id,vote_array):
    vu = voter.voter_dto()
    vu.user_id = user_id
    vu.votation_id = votation_id
    b_has_voted = voter.has_voted(vu)
    if b_has_voted:
        votes = load_vote_by_key(vote_key)
        if len(votes) == 0:
            return False
        delete_votes_by_key(vote_key)
    options_list = option.load_options_by_votation(votation_id)
    for i in range(len(vote_array)):
        o = vote_dto()
        o.vote_key = vote_key
        o.votation_id = votation_id
        o.option_id = options_list[i].option_id
        o.jud_value = vote_array[i]
        insert_dto(o)
    if not b_has_voted:
        voter.insert_dto(vu)
    return True

def load_vote_by_key(vote_key):
    """Returns a vote_dto array"""
    ar = []
    conn = dbmanager.get_connection()
    c = conn.cursor()
    c.execute("select * from vote c where c.vote_key = %s order by option_id", (vote_key,) )
    row = c.fetchone()
    while row:
        o = vote_dto()
        o.vote_key = row['vote_key']
        o.votation_id = row['votation_id']
        o.option_id = row['option_id']
        o.jud_value = row['jud_value']
        ar.append(o)
        row = c.fetchone()
    c.close()
    conn.close()
    return ar

def maj_jud_median_calc(totals_array):
    """The array contains totals for every judgment.
    An array like [12,32,45,67] means: 
    12 votes of 0
    32 votes of 1
    45 votes of 2
    67 votes of 3
    """
    n = len(totals_array)
    element_count = 0
    for i in totals_array:
        element_count = element_count + i
    if element_count == 0:
        return 0
    if element_count/2 == int(element_count/2):
        median_position = element_count/2-1
    else:
        median_position = (element_count+1)/2-1
    #print("median=" + str(median_position))
    partial_count = 0
    result = None
    for i in range(n):
        partial_count = partial_count + totals_array[i]
        if partial_count > median_position:
            result = i
            break
    return result

def trim(totals_array):
    if sum(totals_array) == 0:
        return totals_array
    l = len(totals_array)


class maj_jud_result:
    def __init__(self, option_id, ar):
        self.totals_array = ar
        self.option_id = option_id
        self.option_name = str(option_id)
    def __lt__(self,r2):
        return maj_jud_compare(self.totals_array,r2.totals_array) == -1
    def __gt__(self,r2):
        return maj_jud_compare(self.totals_array,r2.totals_array) == +1
    def __eq__(self,r2):
        return maj_jud_compare(self.totals_array,r2.totals_array) == 0
    def __str__(self):
        return "({}, {})".format(self.option_id, str(self.totals_array))
    def __repr__(self):
        return "({}, {})".format(self.option_id, str(self.totals_array))

def maj_jud_compare(totals_array1, totals_array2):
    """returns +1 f the totals_array1 has a better result than totals_array2.
    returns 0 if the results are the same.
    returns -1 if the totals_array2 has a better result than totals_array1.
    """
    if totals_array1 == totals_array2:
        return 0
    t1 = totals_array1[:]
    t2 = totals_array2[:]
    l1 = len(t1)
    l2 = len(t2)
    median1 = maj_jud_median_calc(t1)
    median2 = maj_jud_median_calc(t2)
    while median1 == median2 and sum(t1) > 0 and sum(t2) > 0:
        #print (t1, median1,t2, median2)
        t1[median1] = t1[median1] - 1
        t2[median2] = t2[median2] - 1
        median1 = maj_jud_median_calc(t1)
        median2 = maj_jud_median_calc(t2)
    #print (t1, median1,t2, median2)
    if median1 > median2:
        return +1
    if median1 < median2:
        return -1
    return 0

def count_votes(votation_id):
    """
    Count number of different vote_key. Its pourpose is to compare with voters.
    """
    result = None
    conn = dbmanager.get_connection()
    c = conn.cursor()
    c.execute("select count(*) from (select distinct vote_key from vote where votation_id = %s) A", (votation_id,) )
    row = c.fetchone()
    if row:
        result = row[0]
    c.close()
    conn.close()
    return result


def count_votes_by_option(votation_id, option_id):
    conn = dbmanager.get_connection()
    ar = []
    for j in range(len(votation.WORDS)):
        c = conn.cursor()
        q = "select count(*) from vote where votation_id = %s and option_id = %s and jud_value = %s"
        c.execute(q, (votation_id, option_id, j))
        row = c.fetchone()
        ar.append( row[0] )
        c.close()
    return ar

def votation_counting(v):
    option_list = option.load_options_by_votation(v.votation_id)
    conn = dbmanager.get_connection()
    counting = []
    for o in option_list:
        ar = count_votes_by_option(v.votation_id,o.option_id)
        m = maj_jud_result(o.option_id,ar)
        m.option_name = o.option_name
        counting.append(m)
    counting.sort()       
    counting.reverse()     
    conn.close()
    return counting

