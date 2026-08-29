import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
import itertools

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup([Permutation(0,1)(2,3), Permutation(0,2)(1,3)])
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = SymmetricGroup(1)

CONDITION_LABELS = [
    "H_1: G is a permutation group acting on a set \\Omega",
    "H_2: k is an integer strictly greater than 1",
    "¬Q: The equivalence between k-transitivity and the recursive condition fails"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        G, k = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    try:
        h2 = isinstance(k, int) and k > 1
    except Exception:
        h2 = False
        
    try:
        if not (h1 and h2):
            return [h1, h2, False]
            
        domain = set(range(G.degree))
        
        def is_k_trans(grp, k_val, dom):
            dom = set(dom)
            if k_val == 0: return True
            if k_val == 1 and len(dom) == 0: return True
            if len(dom) < k_val: return False
            
            k_tuples = list(itertools.permutations(dom, k_val))
            if not k_tuples: return True
            
            start_tuple = k_tuples[0]
            orbit = set([start_tuple])
            queue = [start_tuple]
            
            while queue:
                curr = queue.pop(0)
                for g in grp.generators:
                    nxt = tuple(g(x) if x < g.size else x for x in curr)
                    if nxt not in orbit:
                        orbit.add(nxt)
                        queue.append(nxt)
                        
            return len(orbit) == len(k_tuples)
            
        lhs = is_k_trans(G, k, domain)
        
        is_trans = is_k_trans(G, 1, domain)
        if not is_trans:
            rhs = False
        else:
            rhs = True
            for alpha in domain:
                G_alpha = G.stabilizer(alpha)
                dom_minus_alpha = domain - {alpha}
                if not is_k_trans(G_alpha, k - 1, dom_minus_alpha):
                    rhs = False
                    break
                    
        neg_q = (lhs != rhs)
        
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]