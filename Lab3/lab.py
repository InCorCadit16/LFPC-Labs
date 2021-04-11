import itertools
import numpy
import copy

EPS = 'e'
N = ['S', 'A', 'B', 'D']
T = ['a', 'b', 'd']
P = { 
    'S': ['AB'],
    'A': ['d', 'dS', 'aAaAb', EPS],
    'B': ['a', 'aS', 'A'],
    'D': ['Aba']
    }


def remove_e(prods):
    p_e = [k for k in prods if EPS in prods.get(k)]
    new = {k: [all_combs(s, p_e) for s in prods.get(k) if all_combs(s, p_e) != []] for k in prods}
    new = {k: numpy.concatenate(new.get(k)).flat for k in new}
    [prods.get(p).extend(new.get(n)) for p in prods for n in new if p == n]
    result = {k: list(filter(lambda a: a != EPS and a != '', prods.get(k))) for k in prods}
    return {k: list(dict.fromkeys(result.get(k))) for k in result}


def all_combs(source, let):
    inds = [i for i, ltr in enumerate(source) if ltr in let]
    combs = []
    [combs.extend(itertools.combinations(inds, i)) for i in range(1, len(inds) + 1)]
    return [''.join(source[x] for x in range(len(source)) if x not in i) for i in combs]


def remove_renamings(prods):
    ren = {k: list(s for s in prods.get(k) if s in N) for k in prods if list(s for s in prods.get(k) if s in N) != []}
    filtered = {k: list(s for s in prods.get(k) if s not in N) for k in prods}

    for k in ren:
        new = []
        for v in ren.get(k):
            new.extend(filtered.get(v))
        filtered.get(k).extend(new)

    return filtered

def remove_nonprod(prods):
    nonprod = [k for k in prods if is_nonprod(prods.get(k))]
    result = { k: prods.get(k) for k in prods if k not in nonprod }
    return {k: list(r for r in result.get(k) if not result_nonprod(r, nonprod)) for k in result}


def is_terminal(str):
    for s in str:
        if s in N:
            return False
    return True

def is_nonprod(res):
    return len([filter(lambda a: is_terminal(a), res)]) == 0

def result_nonprod(s, nonprod):
    return len([(c for c in s if c == n) for n in nonprod]) != 0


def remove_inacc(prods):
    both = list(N)
    both.extend(T)
    res = list(numpy.concatenate([prods.get(k) for k in prods]).flat)
    inacc = list(filter(lambda a: not_in_any(a, res), both))
    return {k: prods.get(k) for k in prods if k not in inacc}


def not_in_any(a, lst):
    for l in lst:
        if a in l:
            return False
    return True


def normalize(prods):
    new = {}
    result = copy.deepcopy(prods)
    for pr in prods.keys():
        for r in prods.get(pr):
            if not is_fixed(r):
                res = fix_rule(r, new)
                new = res[1]
                result.get(pr).remove(r)
                result.get(pr).append(res[0])

    result.update(new)
    return result


def fix_rule(r, exst):
    for c in r:
        if c in T:
            res = list(filter(lambda a: exst.get(a) == c, exst.keys()))
            if len(res) == 0:
                exst.update({str(len(exst)): c})
                r = r.replace(c, str(len(exst) - 1))
                N.append(str(len(exst) - 1))
            else:
                r = r.replace(c, res[0])

    while not is_fixed(r):
        ln = len(r) - len(r) % 2
        pairs = [str(r)[n - 2:n] for n in range(2, ln + 1, 2)]
        for p in pairs:
            res = list(filter(lambda a: exst.get(a) == p, exst.keys()))
            if len(res) == 0:
                exst.update({str(len(exst)): p})
                r = r.replace(p, str(len(exst) - 1))
                N.append(str(len(exst) - 1))
            else:
                r = r.replace(p, res[0])

    return [r, exst]


def is_fixed(s):
    return (len(s) == 1 and s[0] in T) or (len(s) == 2 and s[0] in N and s[1] in N)


if __name__ == '__main__':
    prods = remove_e(P)
    prods = remove_renamings(prods)
    N = list(prods.keys())
    prods = remove_nonprod(prods)
    prods = remove_inacc(prods)
    prods = normalize(prods)
    print(prods)


