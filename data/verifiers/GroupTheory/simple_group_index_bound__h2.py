import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def get_order(G):
    try:
        o = G.order
        if callable(o):
            return o()
        return o
    except Exception:
        return 0

def is_simple(G):
    order = get_order(G)
    if order <= 1:
        return False
    from sympy.ntheory import isprime
    if isprime(order):
        return True
    
    # If non-abelian, it must be perfect to be simple
    try:
        is_ab = G.is_abelian
        if callable(is_ab):
            is_ab = is_ab()
        if not is_ab:
            ds = G.derived_subgroup
            if callable(ds):
                ds = ds()
            if get_order(ds) != order:
                return False
    except Exception:
        pass

    # Verify simplicity by checking the normal closure of every non-identity element
    try:
        elements = list(G.generate())
    except Exception:
        return False

    for g in elements:
        try:
            is_id = g.is_Identity
            if callable(is_id):
                is_id = is_id()
        except Exception:
            is_id = False
            
        if is_id:
            continue
            
        H = PermutationGroup([g])
        while True:
            H_order = get_order(H)
            new_gens = list(H.generators)
            for h in H.generators:
                for gen in G.generators:
                    new_gens.append(gen * h * (~gen))
                    new_gens.append((~gen) * h * gen)
            H = PermutationGroup(new_gens)
            if get_order(H) == H_order:
                break
        if get_order(H) < order:
            return False
    return True

def conditions(witness):
    try:
        G, H = witness
    except Exception:
        return [False, False, False, False, False]
    
    # H1: G and H are finite groups
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)
    except Exception:
        h1 = False

    # H2: G is non-abelian
    try:
        is_ab = G.is_abelian
        if callable(is_ab):
            is_ab = is_ab()
        h2 = not is_ab
    except Exception:
        h2 = False

    # H3: G is simple
    try:
        h3 = is_simple(G)
    except Exception:
        h3 = False

    # H4: H is a subgroup of G
    try:
        h4 = all(G.contains(g) for g in H.generators)
    except Exception:
        h4 = False

    # neg_Q: The order of G does not divide n! / 2
    try:
        g_order = get_order(G)
        h_order = get_order(H)
        n = g_order // h_order
        fact_n = math.factorial(n)
        
        # If n! / 2 is not an integer, |G| cannot divide it.
        if fact_n % 2 != 0:
            neg_q = True
        else:
            half_fact = fact_n // 2
            neg_q = (half_fact % g_order != 0)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are finite groups",
    "H_2: G is non-abelian",
    "H_3: G is simple",
    "H_4: H is a subgroup of G",
    "¬Q: The order of G does not divide n!/2"
]

N_HYP = 4
NEG_Q_INDEX = 4