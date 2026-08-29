import math
import itertools
import functools

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            n = witness.get('n')
            k = witness.get('k')
        else:
            n, k = witness
    except Exception:
        return [False, False]

    try:
        h1 = isinstance(k, int) and k > 0
    except Exception:
        h1 = False

    try:
        if not isinstance(n, int):
            neg_q = False
        elif n < 0:
            neg_q = True
        elif n == 0:
            neg_q = (k != 0)
        else:
            polys = set()
            x = 0
            while True:
                p = (x**2 * (n - 2) - x * (n - 4)) // 2
                if p > k and n >= 2:
                    break
                if p < 0:
                    break
                if 0 <= p <= k:
                    polys.add(p)
                x += 1
            
            polys = sorted(list(polys))
            if 0 in polys:
                polys.remove(0)
            
            if k == 0:
                min_steps = 0
            elif not polys:
                min_steps = float('inf')
            else:
                visited = {0}
                queue = [0]
                steps = 0
                found = False
                while queue and steps <= n:
                    steps += 1
                    next_queue = []
                    for val in queue:
                        for p in polys:
                            nxt = val + p
                            if nxt == k:
                                found = True
                                break
                            if nxt < k and nxt not in visited:
                                visited.add(nxt)
                                next_queue.append(nxt)
                        if found: break
                    if found: break
                    queue = next_queue
                
                if found:
                    min_steps = steps
                else:
                    min_steps = float('inf')
            
            neg_q = min_steps > n
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: k is a positive integer",
    "¬Q: k cannot be written as the sum of at most n n-gonal numbers"
]

N_HYP = 1
NEG_Q_INDEX = 1