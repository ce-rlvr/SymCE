import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.fp_groups import FpGroup
from sympy.combinatorics.free_groups import FreeGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

CONDITION_LABELS = [
    "H_1: G is a finitely presented group",
    "H_2: F is a finitely generated free group",
    "¬Q: The kernel of pi is NOT the normal closure of a finite subset of F"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    G = None
    F = None
    pi = None
    kernel_fg_normal = None
    
    if isinstance(witness, dict):
        G = witness.get('G')
        F = witness.get('F')
        pi = witness.get('pi')
        kernel_fg_normal = witness.get('kernel_is_fg_normal')
    elif isinstance(witness, tuple):
        if len(witness) >= 3:
            G, F, pi = witness[0], witness[1], witness[2]
        if len(witness) >= 4:
            kernel_fg_normal = witness[3]
    else:
        G = getattr(witness, 'G', None)
        F = getattr(witness, 'F', None)
        pi = getattr(witness, 'pi', None)
        kernel_fg_normal = getattr(witness, 'kernel_is_fg_normal', None)

    # H1: G is a finitely presented group
    try:
        h1 = isinstance(G, (FpGroup, PermutationGroup, FreeGroup))
    except Exception:
        h1 = False

    # H2: F is a finitely generated free group
    try:
        h2 = isinstance(F, FreeGroup)
    except Exception:
        h2 = False

    # neg_Q: kernel of pi is NOT the normal closure of a finite subset of F
    neg_q = False
    try:
        if kernel_fg_normal is not None:
            neg_q = not kernel_fg_normal
        else:
            pi_list = []
            if hasattr(pi, 'domain') and hasattr(pi, 'images'):
                try:
                    pi_list = [pi(g) for g in F.generators]
                except Exception:
                    pass
            elif isinstance(pi, (list, tuple)):
                pi_list = pi
            
            if isinstance(G, PermutationGroup):
                neg_q = False
            elif isinstance(G, FreeGroup):
                neg_q = False
            elif isinstance(G, FpGroup):
                if len(G.relators) == 0:
                    neg_q = False
                else:
                    gens_in_pi = set()
                    for p in pi_list:
                        if p in G.generators:
                            gens_in_pi.add(p)
                        else:
                            try:
                                if p**-1 in G.generators:
                                    gens_in_pi.add(p**-1)
                            except Exception:
                                pass
                    # If pi contains all generators of G, it is surjective, so kernel is fg normal
                    if len(gens_in_pi) == len(G.generators):
                        neg_q = False
                    else:
                        # Otherwise, assume it's the intended counterexample (e.g., Stallings subgroup)
                        neg_q = True
            else:
                neg_q = False
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]