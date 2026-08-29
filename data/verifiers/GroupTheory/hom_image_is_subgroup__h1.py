import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

N_HYP = 1
NEG_Q_INDEX = 1
CONDITION_LABELS = [
    "H_1: phi is a group homomorphism from G to H",
    "¬Q: phi(G) is not a subgroup of H"
]

def apply_op(op, x, y):
    if callable(op):
        return op(x, y)
    else:
        return op[(x, y)]

def apply_phi(phi, x):
    if callable(phi):
        return phi(x)
    else:
        return phi[x]

def extract_witness(witness):
    if isinstance(witness, dict):
        return witness['G'], witness['H'], witness['G_op'], witness['H_op'], witness['phi']
    elif isinstance(witness, tuple) and len(witness) == 5:
        return witness
    else:
        return witness.G, witness.H, witness.G_op, witness.H_op, witness.phi

def check_is_group(elements, op):
    if hasattr(elements, 'is_group'):
        if callable(elements.is_group):
            return elements.is_group()
        else:
            return bool(elements.is_group)
    if isinstance(elements, sympy.combinatorics.PermutationGroup):
        return True
        
    elements = list(elements)
    if not elements:
        return False
        
    # Check closure
    for a in elements:
        for b in elements:
            try:
                res = apply_op(op, a, b)
                if res not in elements:
                    return False
            except Exception:
                return False
                
    # Check associativity
    for a in elements:
        for b in elements:
            for c in elements:
                try:
                    if apply_op(op, apply_op(op, a, b), c) != apply_op(op, a, apply_op(op, b, c)):
                        return False
                except Exception:
                    return False
                    
    # Check identity
    identity = None
    for e in elements:
        is_id = True
        for a in elements:
            try:
                if apply_op(op, e, a) != a or apply_op(op, a, e) != a:
                    is_id = False
                    break
            except Exception:
                is_id = False
                break
        if is_id:
            identity = e
            break
            
    if identity is None:
        return False
        
    # Check inverses
    for a in elements:
        has_inv = False
        for b in elements:
            try:
                if apply_op(op, a, b) == identity and apply_op(op, b, a) == identity:
                    has_inv = True
                    break
            except Exception:
                pass
        if not has_inv:
            return False
            
    return True

def conditions(witness):
    # H_1: phi is a group homomorphism from G to H
    try:
        if hasattr(witness, 'is_homomorphism'):
            if callable(witness.is_homomorphism):
                h1 = bool(witness.is_homomorphism())
            else:
                h1 = bool(witness.is_homomorphism)
        else:
            G, H, G_op, H_op, phi = extract_witness(witness)
            h1 = True
            for g in G:
                if apply_phi(phi, g) not in H:
                    h1 = False
                    break
            if h1:
                for g1 in G:
                    for g2 in G:
                        lhs = apply_phi(phi, apply_op(G_op, g1, g2))
                        rhs = apply_op(H_op, apply_phi(phi, g1), apply_phi(phi, g2))
                        if lhs != rhs:
                            h1 = False
                            break
                    if not h1:
                        break
    except Exception:
        h1 = False

    # neg_Q: phi(G) is NOT a subgroup of H
    try:
        if hasattr(witness, 'image_is_subgroup'):
            if callable(witness.image_is_subgroup):
                neg_q = not bool(witness.image_is_subgroup())
            else:
                neg_q = not bool(witness.image_is_subgroup)
        else:
            G, H, G_op, H_op, phi = extract_witness(witness)
            image = []
            for g in G:
                val = apply_phi(phi, g)
                if val not in image:
                    image.append(val)
            
            # For phi(G) to be a subgroup of H, H must be a group and phi(G) must be a group under H's operation.
            H_is_group = check_is_group(H, H_op)
            image_is_group = check_is_group(image, H_op)
            
            Q = H_is_group and image_is_group
            neg_q = not Q
    except Exception:
        neg_q = False

    return [h1, neg_q]