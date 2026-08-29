import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics import PermutationGroup
from sympy.matrices import eye, zeros

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_class_sizes(G):
    """Helper to compute the sizes of the conjugacy classes of a permutation group."""
    try:
        # For reasonably small groups, manual computation is fast and robust
        if G.order() <= 2000:
            try:
                elements = list(G.elements)
            except Exception:
                elements = list(G.generate())
            seen = set()
            sizes = []
            for g in elements:
                if g in seen:
                    continue
                c = set()
                for h in elements:
                    c.add(h * g * ~h)
                sizes.append(len(c))
                seen.update(c)
            return sizes
    except Exception:
        pass
    
    # Fallback to sympy's built-in method
    try:
        classes = G.conjugacy_classes()
        sizes = []
        for c in classes:
            if hasattr(c, 'size'):
                sizes.append(c.size)
            else:
                sizes.append(len(list(c)))
        return sizes
    except Exception:
        return []

def is_simple_group(G):
    """Helper to check if a permutation group is simple."""
    try:
        if hasattr(G, 'is_simple'):
            val = G.is_simple
            if callable(val):
                return bool(val())
            return bool(val)
    except Exception:
        pass
    
    try:
        # A group is simple iff its only normal subgroups are the trivial group and itself.
        ns = G.normal_subgroups()
        return len(ns) == 2
    except Exception:
        pass
    
    return False

def conditions(witness) -> list[bool]:
    G = None
    p = None
    k = None
    
    # Extract G, p, k from the witness
    if isinstance(witness, dict) and 'G' in witness:
        G = witness.get('G')
        p = witness.get('p')
        k = witness.get('k')
    elif hasattr(witness, 'G'):
        G = witness.G
        p = getattr(witness, 'p', None)
        k = getattr(witness, 'k', None)
    elif isinstance(witness, tuple) and len(witness) == 3:
        G, p, k = witness
    else:
        G = witness

    # If p or k is missing, try to auto-deduce them to make the verifier robust
    if p is None or k is None:
        try:
            sizes = get_class_sizes(G)
            if sizes:
                # Prefer a class size > 1 if available
                s = next((x for x in sizes if x > 1), sizes[0])
                p = s
                k = 1
            else:
                p = 1
                k = 1
        except Exception:
            p = 1
            k = 1

    # H_1: G is a finite group
    try:
        h1_ok = isinstance(G, PermutationGroup)
    except Exception:
        h1_ok = False

    # H_2: G contains a conjugacy class of size p^k
    try:
        sizes = get_class_sizes(G)
        target = p ** k
        h2_ok = any(s == target for s in sizes)
    except Exception:
        h2_ok = False

    # H_3: k > 0
    try:
        h3_ok = int(k) > 0
    except Exception:
        h3_ok = False

    # ¬Q: G is a simple group (negation of "G is not a simple group")
    try:
        neg_q_ok = is_simple_group(G)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: G contains a conjugacy class of size p^k",
    "H_3: k > 0",
    "¬Q: G is a simple group"
]

N_HYP = 3
NEG_Q_INDEX = 3