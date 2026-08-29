import math
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
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

def conditions(witness) -> list[bool]:
    h1, h2, h3, q = False, False, False, True

    def get_bool_attr(obj, attr):
        if hasattr(obj, attr):
            val = getattr(obj, attr)
            return bool(val() if callable(val) else val)
        return None

    def is_sympy_hom(obj):
        return hasattr(obj, 'domain') and hasattr(obj, 'codomain') and hasattr(obj, 'image')

    try:
        # Extract f, G, H from the witness
        if is_sympy_hom(witness):
            f = witness
            G = witness.domain
            H = witness.codomain
        elif isinstance(witness, tuple) and len(witness) == 3:
            f, G, H = witness
        elif isinstance(witness, dict):
            f = witness.get('f')
            G = witness.get('G')
            H = witness.get('H')
        else:
            f = getattr(witness, 'f', witness)
            G = getattr(witness, 'G', None)
            H = getattr(witness, 'H', None)

        # H1: f is a group homomorphism
        if is_sympy_hom(f):
            h1 = True
        else:
            val = get_bool_attr(f, 'is_group_homomorphism')
            if val is not None: 
                h1 = val
            else:
                val = get_bool_attr(witness, 'is_group_homomorphism')
                if val is not None: 
                    h1 = val

        # H2: G is a divisible group
        val = get_bool_attr(G, 'is_divisible')
        if val is not None: 
            h2 = val
        else:
            val = get_bool_attr(witness, 'G_is_divisible')
            if val is not None: 
                h2 = val
            elif hasattr(G, 'order') and callable(G.order):
                try:
                    # The only finite divisible group is the trivial group
                    h2 = (G.order() == 1)
                except Exception:
                    pass

        # H3: H is a finite group
        if isinstance(H, PermutationGroup):
            h3 = True
        elif hasattr(H, 'order') and callable(H.order):
            try:
                h3 = (H.order() < math.inf)
            except Exception:
                pass
        else:
            val = get_bool_attr(H, 'is_finite')
            if val is not None: 
                h3 = val
            else:
                val = get_bool_attr(witness, 'H_is_finite')
                if val is not None: 
                    h3 = val

        # Q: Image of f is the trivial subgroup of H
        val = get_bool_attr(f, 'image_is_trivial')
        if val is not None: 
            q = val
        else:
            val = get_bool_attr(witness, 'image_is_trivial')
            if val is not None: 
                q = val
            elif hasattr(f, 'image'):
                img = f.image() if callable(f.image) else f.image
                if hasattr(img, 'order') and callable(img.order):
                    q = (img.order() == 1)
                elif hasattr(img, '__len__'):
                    q = (len(img) == 1)
                else:
                    val2 = get_bool_attr(img, 'is_trivial')
                    if val2 is not None: 
                        q = val2
            elif isinstance(f, dict):
                q = (len(set(f.values())) == 1)

    except Exception:
        pass

    return [bool(h1), bool(h2), bool(h3), not bool(q)]

CONDITION_LABELS = [
    "H_1: f is a group homomorphism",
    "H_2: G is a divisible group",
    "H_3: H is a finite group",
    "¬Q: The image of f is not the trivial subgroup of H"
]

N_HYP = 3
NEG_Q_INDEX = 3