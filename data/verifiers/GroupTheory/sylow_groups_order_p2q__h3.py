import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import isprime, primefactors

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def is_sylow_normal(G, prime):
    try:
        order_G = G.order() if callable(G.order) else G.order
        if order_G % prime != 0:
            return True
        
        # Try using SymPy's built-in sylow_subgroup and check normality via generators
        if hasattr(G, 'sylow_subgroup'):
            P = G.sylow_subgroup(prime)
            is_normal = True
            for g in G.generators:
                for h in P.generators:
                    conj = g * h * (~g)
                    if conj not in P:
                        is_normal = False
                        break
                if not is_normal:
                    break
            return is_normal
    except Exception:
        pass
    
    # Fallback: A Sylow p-subgroup is normal iff the number of elements of p-power order equals the order of the Sylow p-subgroup
    try:
        order_G = G.order() if callable(G.order) else G.order
        pk = 1
        temp = order_G
        while temp % prime == 0:
            pk *= prime
            temp //= prime
        
        count = 0
        elements = G.elements if hasattr(G, 'elements') else G.generate()
        for g in elements:
            g_order = g.order() if callable(g.order) else g.order
            if pk % g_order == 0:
                count += 1
        return count == pk
    except Exception:
        return False

def conditions(witness):
    G, p, q = None, None, None
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            G, p, q = witness
        elif isinstance(witness, dict):
            G = witness.get('G')
            p = witness.get('p')
            q = witness.get('q')
        else:
            G = witness
    except Exception:
        pass

    # If p and q are not provided, try to find a pair that makes the negated conclusion True
    if G is not None and p is None and q is None:
        try:
            order_G = G.order() if callable(G.order) else G.order
            factors = primefactors(order_G)
            found = False
            for p_cand in factors:
                for q_cand in factors:
                    if p_cand != q_cand:
                        if not is_sylow_normal(G, p_cand) and not is_sylow_normal(G, q_cand):
                            p, q = p_cand, q_cand
                            found = True
                            break
                if found:
                    break
            if not found:
                if len(factors) >= 2:
                    p, q = factors[0], factors[1]
                else:
                    p, q = 2, 3
        except Exception:
            p, q = 2, 3

    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: p and q are distinct prime numbers
    try:
        h2 = bool(isprime(p) and isprime(q) and (p != q))
    except Exception:
        h2 = False

    # ¬Q: Neither the Sylow p-subgroup of G is normal in G, nor the Sylow q-subgroup of G is normal in G
    try:
        p_normal = is_sylow_normal(G, p)
        q_normal = is_sylow_normal(G, q)
        neg_q = bool((not p_normal) and (not q_normal))
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: p and q are distinct prime numbers",
    "¬Q: Neither the Sylow p-subgroup of G is normal in G, nor the Sylow q-subgroup of G is normal in G"
]

N_HYP = 2
NEG_Q_INDEX = 2