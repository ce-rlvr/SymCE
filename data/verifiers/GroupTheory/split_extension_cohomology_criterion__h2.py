import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
import itertools

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def eval_c(c, g, h):
    if isinstance(c, dict):
        if (g, h) in c:
            return c[(g, h)]
        else:
            raise ValueError("Missing cocycle value")
    else:
        return c(g, h)

def eval_action(action, g, a):
    if action is None:
        return a
    if isinstance(action, dict):
        return action.get((g, a), a)
    return action(g, a)

def check_cocycle(Q, A, c, action=None):
    Q_elems = list(Q.elements)
    for g in Q_elems:
        for h in Q_elems:
            for k in Q_elems:
                chk = eval_c(c, h, k)
                term1 = eval_action(action, g, chk)
                term2 = eval_c(c, g, h * k)
                left = term1 * term2
                
                term3 = eval_c(c, g, h)
                term4 = eval_c(c, g * h, k)
                right = term3 * term4
                
                if left != right:
                    return False
    return True

def is_coboundary(Q, A, c, action=None):
    Q_elems = list(Q.elements)
    A_elems = list(A.elements)
    Q_non_id = [g for g in Q_elems if g != Q.identity]
    for b_vals in itertools.product(A_elems, repeat=len(Q_non_id)):
        b = {Q.identity: A.identity}
        for g, val in zip(Q_non_id, b_vals):
            b[g] = val
        
        is_cob = True
        for g in Q_elems:
            for h in Q_elems:
                bg = b[g]
                bh = b[h]
                bgh = b[g * h]
                act_bh = eval_action(action, g, bh)
                expected = bg * act_bh * (bgh**-1)
                if eval_c(c, g, h) != expected:
                    is_cob = False
                    break
            if not is_cob:
                break
        if is_cob:
            return True
    return False

def make_permutation_group(elems, mult_func):
    n = len(elems)
    elem_to_idx = {e: i for i, e in enumerate(elems)}
    perms = []
    for x in elems:
        p = [0] * n
        for y in elems:
            xy = mult_func(x, y)
            p[elem_to_idx[y]] = elem_to_idx[xy]
        perms.append(Permutation(p))
    return PermutationGroup(perms)

def check_semidirect_isomorphic(A, Q, G, action=None):
    A_elems = list(A.elements)
    Q_elems = list(Q.elements)
    S_elems = list(itertools.product(A_elems, Q_elems))
    
    def S_mult(x, y):
        a1, g1 = x
        a2, g2 = y
        act_a2 = eval_action(action, g1, a2)
        return (a1 * act_a2, g1 * g2)
    
    S_group = make_permutation_group(S_elems, S_mult)
    return G.is_isomorphic(S_group)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            A = witness.get("A")
            Q = witness.get("Q")
            G = witness.get("G")
            c = witness.get("c")
            action = witness.get("action", None)
        elif isinstance(witness, tuple):
            if len(witness) == 4:
                A, Q, G, c = witness
                action = None
            elif len(witness) == 5:
                A, Q, G, action, c = witness
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    try:
        h1 = isinstance(A, PermutationGroup) and isinstance(Q, PermutationGroup) and A.is_abelian
    except Exception:
        h1 = False

    try:
        h2 = check_cocycle(Q, A, c, action)
    except Exception:
        h2 = False

    try:
        is_semi = isinstance(G, PermutationGroup) and check_semidirect_isomorphic(A, Q, G, action)
        is_id = is_coboundary(Q, A, c, action)
        neg_q = not (is_semi == is_id)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: A is an abelian group and Q is a group",
    "H_2: c is a valid 2-cocycle from Q x Q to A",
    "neg_Q: The biconditional G is isomorphic to semidirect product iff c is identity is false"
]

N_HYP = 2
NEG_Q_INDEX = 2