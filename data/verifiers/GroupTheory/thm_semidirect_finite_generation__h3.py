import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

# Top-level setup
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def call_or_bool(val, *args):
    if callable(val):
        try:
            return bool(val(*args))
        except TypeError:
            try:
                return bool(val())
            except Exception:
                return False
    return bool(val)

def get_bool_attr(obj, attr, default=True):
    if isinstance(obj, dict) and attr in obj:
        return call_or_bool(obj[attr])
    if hasattr(obj, attr):
        return call_or_bool(getattr(obj, attr))
    return default

def conditions(witness) -> list[bool]:
    # 1. Check if witness is a dict with the exact boolean flags
    if isinstance(witness, dict) and 'is_semidirect_product' in witness:
        try:
            h1 = bool(witness.get('is_semidirect_product', False))
            h2 = bool(witness.get('N_is_finitely_generated', False))
            neg_q = not bool(witness.get('G_is_finitely_generated', True))
            return [h1, h2, neg_q]
        except Exception:
            pass
            
    # 2. Check if witness is an object with the exact boolean flags
    if hasattr(witness, 'is_semidirect_product'):
        try:
            h1 = bool(getattr(witness, 'is_semidirect_product', False))
            h2 = bool(getattr(witness, 'N_is_finitely_generated', False))
            neg_q = not bool(getattr(witness, 'G_is_finitely_generated', True))
            return [h1, h2, neg_q]
        except Exception:
            pass

    # 3. Assume witness is a tuple (G, N, H)
    try:
        G, N, H = witness
    except Exception:
        return [False, False, False]
        
    # H1: G is internal semidirect product of N and H
    h1 = False
    try:
        if isinstance(G, dict) and 'is_internal_semidirect_product' in G:
            h1 = call_or_bool(G['is_internal_semidirect_product'], N, H)
        elif hasattr(G, 'is_internal_semidirect_product'):
            h1 = call_or_bool(G.is_internal_semidirect_product, N, H)
        elif isinstance(G, PermutationGroup) and isinstance(N, PermutationGroup) and isinstance(H, PermutationGroup):
            if N.is_subgroup(G) and N.is_normal(G) and H.is_subgroup(G):
                intersect = N.intersection(H)
                if intersect.order() == 1:
                    gen = list(N.generators) + list(H.generators)
                    if PermutationGroup(gen) == G:
                        h1 = True
        else:
            # Fallback for mock objects
            n_normal = False
            if isinstance(N, dict) and 'is_normal' in N:
                n_normal = call_or_bool(N['is_normal'], G)
            elif hasattr(N, 'is_normal'):
                n_normal = call_or_bool(N.is_normal, G)
            elif isinstance(G, dict) and 'is_normal' in G:
                n_normal = call_or_bool(G['is_normal'], N)
            elif hasattr(G, 'is_normal'):
                n_normal = call_or_bool(G.is_normal, N)
            else:
                n_normal = True
                
            h_sub = False
            if isinstance(H, dict) and 'is_subgroup' in H:
                h_sub = call_or_bool(H['is_subgroup'], G)
            elif hasattr(H, 'is_subgroup'):
                h_sub = call_or_bool(H.is_subgroup, G)
            elif isinstance(G, dict) and 'is_subgroup' in G:
                h_sub = call_or_bool(G['is_subgroup'], H)
            elif hasattr(G, 'is_subgroup'):
                h_sub = call_or_bool(G.is_subgroup, H)
            else:
                h_sub = True
                
            h1 = n_normal and h_sub
    except Exception:
        h1 = False

    # H2: N is finitely generated
    try:
        h2 = get_bool_attr(N, 'is_finitely_generated', default=True)
    except Exception:
        h2 = False

    # neg_Q: G is NOT finitely generated
    try:
        g_fg = get_bool_attr(G, 'is_finitely_generated', default=True)
        neg_q = not g_fg
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is the internal semidirect product of a normal subgroup N and a subgroup H",
    "H_2: N is finitely generated",
    "¬Q: G is not finitely generated"
]

N_HYP = 2
NEG_Q_INDEX = 2