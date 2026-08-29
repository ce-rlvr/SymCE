import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.combinatorics import Permutation, PermutationGroup
from sympy import isprime

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

def conditions(witness):
    if isinstance(witness, tuple) or isinstance(witness, list):
        G = witness[0]
    else:
        G = witness

    def get_order(grp):
        return grp.order() if callable(grp.order) else grp.order

    def get_degree(grp):
        return grp.degree() if callable(grp.degree) else grp.degree

    def get_generators(grp):
        return grp.generators() if callable(grp.generators) else grp.generators

    def get_is_abelian(grp):
        return grp.is_abelian() if callable(grp.is_abelian) else grp.is_abelian

    def is_id(g):
        res = getattr(g, 'is_Identity', None)
        if res is not None:
            return res() if callable(res) else res
        if hasattr(g, 'support'):
            supp = g.support() if callable(g.support) else g.support
            return len(supp) == 0
        return False

    # H1: G is a perfect group
    try:
        D = G.derived_subgroup()
        H1 = (get_order(D) == get_order(G))
    except Exception:
        H1 = False

    # H2: X is a non-empty set
    try:
        H2 = (get_degree(G) > 0)
    except Exception:
        H2 = False

    # H3: G acts faithfully and primitively on X
    try:
        H3 = G.is_primitive() if callable(G.is_primitive) else G.is_primitive
    except Exception:
        H3 = False

    # H4: There exists x in X such that G_x contains an abelian normal subgroup A of G_x
    try:
        H4 = False
        if get_degree(G) > 0:
            # The trivial subgroup is always an abelian normal subgroup of G_x
            Gx = G.stabilizer(0)
            H4 = True
    except Exception:
        H4 = False

    # ¬Q: G is not a simple group
    try:
        is_simple = None
        order_G = get_order(G)
        if order_G == 1:
            is_simple = False
        else:
            if hasattr(G, 'is_simple'):
                try:
                    res = G.is_simple() if callable(G.is_simple) else G.is_simple
                    if res is not None:
                        is_simple = res
                except Exception:
                    pass
            
            if is_simple is None:
                if get_is_abelian(G):
                    is_simple = isprime(order_G)
                else:
                    is_simple = True
                    for g in get_generators(G):
                        if is_id(g):
                            continue
                        N = G.normal_closure([g])
                        if get_order(N) < order_G:
                            is_simple = False
                            break
                    
                    if is_simple:
                        count = 0
                        elements_iter = G.generate() if hasattr(G, 'generate') else getattr(G, 'elements', [])
                        for g in elements_iter:
                            if is_id(g):
                                continue
                            N = G.normal_closure([g])
                            if get_order(N) < order_G:
                                is_simple = False
                                break
                            count += 1
                            if count > 200:
                                break
                    
                    if is_simple and hasattr(G, 'random'):
                        for _ in range(300):
                            g = G.random()
                            if is_id(g):
                                continue
                            N = G.normal_closure([g])
                            if get_order(N) < order_G:
                                is_simple = False
                                break
        neg_Q = not is_simple
    except Exception:
        neg_Q = False

    return [bool(H1), bool(H2), bool(H3), bool(H4), bool(neg_Q)]

CONDITION_LABELS = [
    "H_1: G is a perfect group",
    "H_2: X is a non-empty set",
    "H_3: G acts faithfully and primitively on X",
    "H_4: There exists x in X such that G_x contains an abelian normal subgroup A of G_x",
    "¬Q: G is not a simple group"
]

N_HYP = 4
NEG_Q_INDEX = 4