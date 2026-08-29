import sympy
from sympy.combinatorics.free_groups import free_group, FreeGroup
from sympy.combinatorics.fp_groups import FpGroup
from sympy.combinatorics.homomorphisms import homomorphism, GroupHomomorphism
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy import oo, eye, zeros

# Top-level setup for witness expressions
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

# Provide standard infinite groups
F1, x_gen = free_group("x")
Z = FpGroup(F1, [])

CONDITION_LABELS = [
    "H_1: f is a group homomorphism",
    "H_2: ker(f) is a finite group",
    "¬Q: G is an infinite group"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    # H_1: f is a group homomorphism
    try:
        h1_ok = isinstance(witness, GroupHomomorphism)
    except Exception:
        h1_ok = False

    # H_2: ker(f) is a finite group
    h2_ok = False
    if h1_ok:
        try:
            if hasattr(witness, 'is_injective') and witness.is_injective():
                h2_ok = True
        except Exception:
            pass
        
        if not h2_ok:
            try:
                G = witness.domain
                # If G is Z (or any free group on 1 generator) and H is a free group,
                # any non-trivial homomorphism is injective, hence has a trivial (finite) kernel.
                if isinstance(G, (FpGroup, FreeGroup)) and len(G.generators) == 1:
                    H = witness.codomain
                    if isinstance(H, (FpGroup, FreeGroup)) and len(getattr(H, 'relators', [])) == 0:
                        g = G.generators[0]
                        if witness(g) != H.identity:
                            h2_ok = True
            except Exception:
                pass
                
        if not h2_ok:
            try:
                G = witness.domain
                H = witness.codomain
                # If f is the identity homomorphism, the kernel is trivial (finite)
                if G == H:
                    if all(witness(g) == g for g in G.generators):
                        h2_ok = True
            except Exception:
                pass

        if not h2_ok:
            try:
                ker = witness.kernel()
                if hasattr(ker, 'order') and ker.order() != oo:
                    h2_ok = True
                elif hasattr(ker, 'generators'):
                    if len(ker.generators) == 0 or all(g.is_identity for g in ker.generators):
                        h2_ok = True
            except Exception:
                pass

    # ¬Q: G is an infinite group
    neg_q_ok = False
    if h1_ok:
        try:
            G = witness.domain
            if hasattr(G, 'order') and G.order() == oo:
                neg_q_ok = True
            else:
                if isinstance(G, FreeGroup):
                    neg_q_ok = True
                elif isinstance(G, FpGroup):
                    if len(G.relators) == 0 and len(G.generators) > 0:
                        neg_q_ok = True
        except Exception:
            pass

    return [h1_ok, h2_ok, neg_q_ok]