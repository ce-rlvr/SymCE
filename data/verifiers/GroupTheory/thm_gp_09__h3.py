import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools
import z3

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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "A subgroup of a finitely presented group is finitely presented."
    
    The witness should represent a pair (G, H) where G is a finitely presented group
    and H is a subgroup of G that is NOT finitely presented.
    """
    try:
        if isinstance(witness, dict):
            G = witness.get('G', witness.get('group'))
            H = witness.get('H', witness.get('subgroup'))
        elif isinstance(witness, (tuple, list)) and len(witness) == 2:
            G, H = witness
        else:
            H = witness
            G = getattr(H, 'parent', None)
            if G is None:
                return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: G is a finitely presented group
    try:
        h1 = False
        if isinstance(G, str):
            g_lower = G.lower()
            if any(name in g_lower for name in ['f2', 'free group', 'f_2', 'f3', 'f_n', 'f2xf2', 'f2 x f2', 'surface group', 'z', 'cyclic', 'symmetric', 'alternating', 'dihedral', 'group']):
                h1 = True
        elif hasattr(G, 'is_finitely_presented'):
            val = G.is_finitely_presented
            h1 = bool(val() if callable(val) else val)
        elif type(G).__name__ in ['FreeGroup', 'FpGroup', 'SymmetricGroup', 'AlternatingGroup', 'DihedralGroup', 'CyclicGroup', 'PermutationGroup', 'AbelianGroup']:
            h1 = True
        elif isinstance(G, dict) and G.get('is_finitely_presented') is True:
            h1 = True
    except Exception:
        h1 = False

    # H_2: H is a subgroup of G
    try:
        h2 = False
        if isinstance(H, str):
            h_lower = H.lower()
            if any(word in h_lower for word in ['commutator', 'kernel', 'infinite index', 'subgroup', 'trivial']):
                h2 = True
        elif hasattr(H, 'parent'):
            h2 = (H.parent is G or H.parent == G)
        elif hasattr(H, 'is_subgroup'):
            val = H.is_subgroup(G)
            h2 = bool(val() if callable(val) else val)
        elif isinstance(H, dict):
            if H.get('parent') is G or H.get('parent') == G:
                h2 = True
            elif H.get('is_subgroup') is True:
                h2 = True
            elif H.get('is_subgroup_of') is G or H.get('is_subgroup_of') == G:
                h2 = True
    except Exception:
        h2 = False

    # neg_Q: H is NOT finitely presented
    try:
        neg_q = False
        if isinstance(H, str):
            h_lower = H.lower()
            g_str = G.lower() if isinstance(G, str) else (G.get('name', '').lower() if isinstance(G, dict) else '')
            
            if 'commutator' in h_lower:
                if any(n in g_str for n in ['f2', 'free group', 'f_2', 'f3', 'f_n']) or \
                   (type(G).__name__ == 'FreeGroup' and len(G.generators) >= 2):
                    neg_q = True
            elif 'kernel' in h_lower:
                if any(n in g_str for n in ['f2xf2', 'f2 x f2']) or \
                   (type(G).__name__ == 'FpGroup'):
                    neg_q = True
            elif any(w in h_lower for w in ['infinite index', 'not finitely presented', 'not fp', 'infinite rank']):
                if any(n in g_str for n in ['f2', 'free group', 'f_2', 'f3', 'f_n', 'f2xf2', 'f2 x f2']) or \
                   (type(G).__name__ == 'FreeGroup' and len(G.generators) >= 2) or \
                   (type(G).__name__ == 'FpGroup'):
                    neg_q = True
        elif hasattr(H, 'is_finitely_presented'):
            val = H.is_finitely_presented
            fp = bool(val() if callable(val) else val)
            neg_q = not fp
        elif isinstance(H, dict) and 'is_finitely_presented' in H:
            neg_q = not bool(H['is_finitely_presented'])
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finitely presented group",
    "H_2: H is a subgroup of G",
    "¬Q: H is not finitely presented"
]

N_HYP = 2
NEG_Q_INDEX = 2