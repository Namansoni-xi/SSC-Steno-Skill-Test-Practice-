import re

def simple_distance(a, b):
    return abs(len(a) - len(b)) + sum(1 for x, y in zip(a, b) if x != y)

def is_spelling(m, u):
    return simple_distance(m.lower(), u.lower()) <= 2

def is_plural_issue(m, u):
    return m.lower()+"s" == u.lower() or u.lower()+"s" == m.lower()

def evaluate(master, user):

    master_words = master.strip().split()
    user_words = user.strip().split()

    full = 0
    half = 0

    i = j = 0

    while i < len(master_words) and j < len(user_words):

        m = master_words[i]
        u = user_words[j]

        if m == u:
            i += 1
            j += 1
            continue

        if is_spelling(m, u):
            half += 1

        elif is_plural_issue(m, u):
            half += 1

        else:
            full += 1

        i += 1
        j += 1

    full += abs(len(master_words) - len(user_words))

    master_punct = re.findall(r'[.,!?]', master)
    user_punct = re.findall(r'[.,!?]', user)

    half += abs(len(master_punct) - len(user_punct))

    total_words = len(master_words)

    error = ((full + half/2) * 100) / total_words

    return {
        "full": full,
        "half": half,
        "error%": round(error, 2),
        "total_words": total_words
    }
