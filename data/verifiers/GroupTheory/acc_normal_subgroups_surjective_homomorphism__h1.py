import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
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
    "H_1: f: G \\to H is a surjective group homomorphism",
    "H_2: G satisfies the ascending chain condition on normal subgroups",
    "¬Q: H does not satisfy the ascending chain condition on normal subgroups"
]

N_HYP = 2
NEG_Q_INDEX = 2

def is_finite_iterable(obj):
    if isinstance(obj, (list, set, tuple, dict)):
        return True
    if hasattr(obj, 'is_finite'):
        val = obj.is_finite() if callable(obj.is_finite) else obj.is_finite
        if val: return True
    if hasattr(obj, 'order'):
        try:
            ord_val = obj.order() if callable(obj.order) else obj.order
            if ord_val < float('inf'): return True
        except Exception:
            pass
    if isinstance(obj, PermutationGroup):
        return True
    return False

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            G, H, f = witness
        elif isinstance(witness, dict):
            G, H, f = witness['G'], witness['H'], witness['f']
        else:
            G, H, f = witness.G, witness.H, witness.f
    except Exception:
        return [False, False, False]

    def check_surjective_homomorphism(G, H, f):
        if hasattr(f, 'is_surjective') and hasattr(f, 'is_homomorphism'):
            is_surj = f.is_surjective() if callable(f.is_surjective) else f.is_surjective
            is_hom = f.is_homomorphism() if callable(f.is_homomorphism) else f.is_homomorphism
            if is_surj is not None and is_hom is not None:
                return bool(is_surj and is_hom)
                
        if not (is_finite_iterable(G) and is_finite_iterable(H)):
            if hasattr(witness, 'is_surjective_homomorphism'):
                val = witness.is_surjective_homomorphism
                return bool(val() if callable(val) else val)
            return False
            
        G_elements = list(G.elements) if hasattr(G, 'elements') else list(G)
        H_elements = list(H.elements) if hasattr(H, 'elements') else list(H)
        
        image = []
        for g in G_elements:
            val = f(g) if callable(f) else f[g]
            if val not in image:
                image.append(val)
                
        if len(image) != len(H_elements):
            return False
            
        for h in H_elements:
            if h not in image:
                return False
                
        for g1 in G_elements:
            for g2 in G_elements:
                val1 = f(g1) if callable(f) else f[g1]
                val2 = f(g2) if callable(f) else f[g2]
                g1g2 = g1 * g2
                val12 = f(g1g2) if callable(f) else f[g1g2]
                if val12 != val1 * val2:
                    return False
        return True

    def satisfies_acc_normal(group):
        if hasattr(group, 'satisfies_acc_normal'):
            val = group.satisfies_acc_normal
            return bool(val() if callable(val) else val)
        if hasattr(group, 'has_acc_normal'):
            val = group.has_acc_normal
            return bool(val() if callable(val) else val)
        if is_finite_iterable(group):
            return True
        return False

    try:
        h1 = check_surjective_homomorphism(G, H, f)
    except Exception:
        h1 = False

    try:
        h2 = satisfies_acc_normal(G)
    except Exception:
        h2 = False

    try:
        neg_q = not satisfies_acc_normal(H)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]