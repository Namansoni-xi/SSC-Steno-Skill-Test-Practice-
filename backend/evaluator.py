def remove_dot(w):
    return w.replace(".", "").lower()

def evaluate(master, user):

    m = master.split()
    u = user.split()

    i = j = 0
    full = 0
    half = 0

    while i < len(m) and j < len(u):

        mw = m[i]
        uw = u[j]

        if mw == uw:
            i += 1
            j += 1
            continue

        # full stop mistake
        if remove_dot(mw) == remove_dot(uw):
            half += 1
            i += 1
            j += 1
            continue

        # missing
        if i+1 < len(m) and m[i+1] == uw:
            full += 1
            i += 1
            continue

        # extra
        if j+1 < len(u) and mw == u[j+1]:
            full += 1
            j += 1
            continue

        # wrong word
        full += 1
        i += 1
        j += 1

    full += (len(m)-i) + (len(u)-j)

    error = ((full + half/2) / len(m)) * 100

    return {
        "full": full,
        "half": half,
        "error%": round(error,2)
    }


def highlight(master, user):

    m = master.split()
    u = user.split()

    i = j = 0
    out = []

    while i < len(m) and j < len(u):

        mw = m[i]
        uw = u[j]

        if mw == uw:
            out.append(f"<span style='color:green'>{uw}</span>")
            i += 1
            j += 1
            continue

        if remove_dot(mw) == remove_dot(uw):
            out.append(f"<span style='color:orange'>{uw}</span>")
            i += 1
            j += 1
            continue

        if i+1 < len(m) and m[i+1] == uw:
            out.append(f"<span style='color:red'>[missing:{mw}]</span>")
            i += 1
            continue

        if j+1 < len(u) and mw == u[j+1]:
            out.append(f"<span style='color:red'>[extra:{uw}]</span>")
            j += 1
            continue

        out.append(f"<span style='color:red'>{uw}</span>")
        i += 1
        j += 1

    return " ".join(out)

def breakdown(master, user):

    m = master.split()
    u = user.split()

    result = []

    for i in range(max(len(m), len(u))):
        mw = m[i] if i < len(m) else ""
        uw = u[i] if i < len(u) else ""

        if mw == uw:
            result.append({"word": uw, "status": "correct"})
        else:
            result.append({"word": uw, "status": "wrong"})

    return result
