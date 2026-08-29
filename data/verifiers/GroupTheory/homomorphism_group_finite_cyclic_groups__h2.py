import math
from itertools import product
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
)
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import sympy.abc

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: n and m are positive integers",
    "H_2: H is the cyclic group Z/mZ",
    "¬Q: Hom(G, H) is not isomorphic to Z/gcd(n,m)Z"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            n = witness.get('n')
            m = witness.get('m')
            G = witness.get('G')
            H = witness.get('H')
        else:
            n, m, G, H = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1 = (int(n) == n) and (int(m) == m) and (n > 0) and (m > 0)
    except Exception:
        h1 = False
        
    try:
        h2 = False
        if getattr(H, 'is_group', False) and H.order() == m:
            for g in H.generate():
                if g.order() == m:
                    h2 = True
                    break
    except Exception:
        h2 = False
        
    try:
        neg_q = False
        if h1 and h2 and getattr(G, 'is_group', False):
            m_int = int(m)
            n_int = int(n)
            gens = list(G.generators)
            k = len(gens)
            if k == 0:
                identity = list(G.generate())[0]
            else:
                identity = gens[0]**0
                
            elements = [identity]
            seen = {identity: [0]*k}
            relations = []
            
            head = 0
            while head < len(elements) and head < 2000:
                curr = elements[head]
                head += 1
                for i, g in enumerate(gens):
                    nxt = curr * g
                    if nxt not in seen:
                        new_exp = list(seen[curr])
                        new_exp[i] += 1
                        seen[nxt] = new_exp
                        elements.append(nxt)
                    else:
                        rel = list(seen[curr])
                        rel[i] += 1
                        for j in range(k):
                            rel[j] -= seen[nxt][j]
                        rel = [x % m_int for x in rel]
                        if any(x != 0 for x in rel):
                            relations.append(rel)
                            
            if head == 2000:
                return [h1, h2, False]
                
            unique_relations = []
            for r in relations:
                if r not in unique_relations:
                    unique_relations.append(r)
                    
            homs = []
            for assignment in product(range(m_int), repeat=k):
                valid = True
                for rel in unique_relations:
                    val = sum(rel[j] * assignment[j] for j in range(k))
                    if val % m_int != 0:
                        valid = False
                        break
                if valid:
                    homs.append(assignment)
                    
            target_size = math.gcd(n_int, m_int)
            if len(homs) != target_size:
                neg_q = True
            else:
                max_ord = 1
                for h in homs:
                    g_val = m_int
                    for x in h:
                        g_val = math.gcd(g_val, x)
                    ord_h = m_int // g_val
                    if ord_h > max_ord:
                        max_ord = ord_h
                if max_ord < len(homs):
                    neg_q = True
                else:
                    neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]