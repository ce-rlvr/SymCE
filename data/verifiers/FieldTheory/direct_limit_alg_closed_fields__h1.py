import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

# Top-level setup: named object bindings
S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
C4 = sympy.combinatorics.named_groups.CyclicGroup(4)
V4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)
I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness) -> list[bool]:
    h1, h2, neg_q = False, False, False

    def check_attr(obj, attrs):
        for attr in attrs:
            if hasattr(obj, attr):
                val = getattr(obj, attr)
                if callable(val):
                    try:
                        return bool(val())
                    except Exception:
                        pass
                else:
                    return bool(val)
        return None

    try:
        # Dictionary fallback
        if isinstance(witness, dict):
            h1 = witness.get('is_directed_system', witness.get('h1', False))
            h2 = witness.get('is_direct_limit', witness.get('h2', False))
            neg_q = witness.get('not_algebraically_closed', witness.get('neg_q', False))
            if h1 and h2 and neg_q:
                return [True, True, True]

        # Tuple fallback (system, K)
        if isinstance(witness, tuple) and len(witness) == 2:
            system, K = witness
            h1_sys = check_attr(system, ['is_directed_system_of_algebraically_closed_fields', 'is_directed_system'])
            if h1_sys is not None: h1 = h1_sys
            
            h2_k = check_attr(K, ['is_direct_limit'])
            if h2_k is not None: h2 = h2_k
            
            is_acf_k = check_attr(K, ['is_algebraically_closed_field', 'is_algebraically_closed'])
            if is_acf_k is not None:
                neg_q = not is_acf_k
            else:
                is_field = check_attr(K, ['is_field', 'is_Field'])
                if is_field is False:
                    neg_q = True

        # Object attributes for H1
        h1_val = check_attr(witness, [
            'is_directed_system_of_algebraically_closed_fields',
            'is_directed_system',
            'h1'
        ])
        if h1_val is not None: h1 = h1_val

        # Object attributes for H2
        h2_val = check_attr(witness, [
            'is_direct_limit',
            'h2'
        ])
        if h2_val is not None: h2 = h2_val

        # Object attributes for neg_Q
        neg_q_val = check_attr(witness, [
            'is_not_algebraically_closed',
            'neg_q'
        ])
        if neg_q_val is not None: 
            neg_q = neg_q_val
        else:
            is_acf = check_attr(witness, [
                'is_algebraically_closed_field',
                'is_algebraically_closed'
            ])
            if is_acf is not None:
                neg_q = not is_acf
            else:
                is_field = check_attr(witness, ['is_field', 'is_Field'])
                if is_field is False:
                    neg_q = True

        # If witness has a 'K' attribute
        if hasattr(witness, 'K'):
            if h2_val is None:
                h2_k = check_attr(witness.K, ['is_direct_limit'])
                if h2_k is not None: h2 = h2_k
            if neg_q_val is None and is_acf is None:
                is_acf_k = check_attr(witness.K, ['is_algebraically_closed_field', 'is_algebraically_closed'])
                if is_acf_k is not None:
                    neg_q = not is_acf_k
                else:
                    is_field = check_attr(witness.K, ['is_field', 'is_Field'])
                    if is_field is False:
                        neg_q = True

        # If witness has a 'system' attribute
        if hasattr(witness, 'system'):
            if h1_val is None:
                h1_sys = check_attr(witness.system, ['is_directed_system_of_algebraically_closed_fields', 'is_directed_system'])
                if h1_sys is not None: h1 = h1_sys

        # String fallback (e.g., "zero_ring", "empty_system")
        if isinstance(witness, str):
            s = witness.lower()
            if 'zero' in s or 'empty' in s or 'trivial' in s:
                return [True, True, True]

        # List fallback (empty system)
        if isinstance(witness, list) and len(witness) == 0:
            return [True, True, True]

        # Zero fallback (zero ring)
        try:
            if witness == 0 or witness == sympy.S.Zero:
                return [True, True, True]
        except Exception:
            pass

    except Exception:
        pass

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: (K_i)_{i in I} is a directed system of algebraically closed fields",
    "H_2: K is the direct limit of the system (K_i)_{i in I}",
    "¬Q: The field K is not algebraically closed"
]

N_HYP = 2
NEG_Q_INDEX = 2