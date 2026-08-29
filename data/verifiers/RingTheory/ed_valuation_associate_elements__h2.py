import sympy
from sympy import eye, zeros, Rational, Integer
from sympy.abc import x, y, z
import math
import itertools
import functools

from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: R is a Euclidean domain with a Euclidean function d satisfying d(xy) >= d(x) for all non-zero x, y in R",
    "H_2: The element a is an associate of b",
    "¬Q: The Euclidean valuations are not equal, meaning d(a) != d(b) or undefined"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        # Extract components from dictionary or object
        if isinstance(witness, dict):
            elements = witness.get('elements', None)
            zero = witness.get('zero', 0)
            one = witness.get('one', 1)
            add = witness.get('add', lambda x, y: x + y)
            mul = witness.get('mul', lambda x, y: x * y)
            d = witness.get('d', abs)
            a = witness.get('a', 0)
            b = witness.get('b', 0)
        else:
            elements = getattr(witness, 'elements', None)
            zero = getattr(witness, 'zero', 0)
            one = getattr(witness, 'one', 1)
            add = getattr(witness, 'add', lambda x, y: x + y)
            mul = getattr(witness, 'mul', lambda x, y: x * y)
            d = getattr(witness, 'd', abs)
            a = getattr(witness, 'a', 0)
            b = getattr(witness, 'b', 0)
            
        if elements is not None:
            # Check H1: Euclidean domain and d(xy) >= d(x)
            is_domain = True
            if one == zero:
                is_domain = False
            else:
                for elem_x in elements:
                    if elem_x != zero:
                        for elem_y in elements:
                            if elem_y != zero:
                                if mul(elem_x, elem_y) == zero:
                                    is_domain = False
            
            is_euclidean = True
            if is_domain:
                for elem_x in elements:
                    for elem_y in elements:
                        if elem_y != zero:
                            found = False
                            for q in elements:
                                yq = mul(elem_y, q)
                                for r in elements:
                                    if add(yq, r) == elem_x:
                                        if r == zero:
                                            found = True
                                            break
                                        try:
                                            if d(r) < d(elem_y):
                                                found = True
                                                break
                                        except Exception:
                                            pass
                                if found:
                                    break
                            if not found:
                                is_euclidean = False
                                break
                    if not is_euclidean:
                        break
            
            d_condition = True
            if is_domain and is_euclidean:
                for elem_x in elements:
                    if elem_x != zero:
                        for elem_y in elements:
                            if elem_y != zero:
                                xy = mul(elem_x, elem_y)
                                try:
                                    if d(xy) < d(elem_x):
                                        d_condition = False
                                except Exception:
                                    d_condition = False
            
            h1 = is_domain and is_euclidean and d_condition
            
            # Check H2: a is an associate of b
            units = []
            for u in elements:
                for v in elements:
                    if mul(u, v) == one:
                        units.append(u)
                        break
            
            for u in units:
                if mul(u, b) == a:
                    h2 = True
                    break
        else:
            # Fallback for H1 if elements are not explicitly provided
            if hasattr(witness, 'is_euclidean_domain'):
                h1_val = witness.is_euclidean_domain
                h1 = h1_val() if callable(h1_val) else h1_val
            elif isinstance(witness, dict) and 'is_euclidean_domain' in witness:
                h1_val = witness['is_euclidean_domain']
                h1 = h1_val() if callable(h1_val) else h1_val
            else:
                try:
                    _ = d(one)
                    h1 = True
                except Exception:
                    h1 = False
                    
            # Fallback for H2 if elements are not explicitly provided
            if hasattr(witness, 'is_associate'):
                h2_val = witness.is_associate
                h2 = h2_val(a, b) if callable(h2_val) else h2_val
            elif isinstance(witness, dict) and 'is_associate' in witness:
                h2_val = witness['is_associate']
                h2 = h2_val(a, b) if callable(h2_val) else h2_val
            else:
                try:
                    h2 = (a == b or a == mul(getattr(witness, 'minus_one', -1), b))
                except Exception:
                    try:
                        h2 = (a == b or a == -b)
                    except Exception:
                        h2 = False
                        
    except Exception:
        pass

    # Check negated conclusion: d(a) != d(b) or undefined
    try:
        val_a = d(a)
        val_b = d(b)
        if val_a != val_b:
            neg_q = True
    except Exception:
        # If d(a) or d(b) is undefined (e.g., d(0) in a standard Euclidean function), the conclusion fails
        neg_q = True

    return [bool(h1), bool(h2), bool(neg_q)]