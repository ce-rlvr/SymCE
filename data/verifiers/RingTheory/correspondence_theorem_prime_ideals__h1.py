import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools

# Top-level setup for potential witness expressions
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
    "H_1: I is a proper ideal of R",
    "H_2: \\pi: R \\to R/I is the canonical projection homomorphism",
    "¬Q: The mapping P \\mapsto \\pi(P) is NOT a bijection between prime ideals of R containing I and prime ideals of R/I"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    # 1. Try dictionary duck-typing
    try:
        if isinstance(witness, dict) and 'H1' in witness:
            h1 = bool(witness.get('H1', False))
            h2 = bool(witness.get('H2', False))
            neg_q = not bool(witness.get('Q', True))
            return [h1, h2, neg_q]
    except Exception:
        pass

    # 2. Try object duck-typing
    try:
        if hasattr(witness, 'is_proper_ideal'):
            h1 = bool(witness.is_proper_ideal())
            h2 = bool(witness.is_canonical_projection())
            neg_q = not bool(witness.is_bijection())
            return [h1, h2, neg_q]
    except Exception:
        pass

    # 3. Try finite ring representation: (elements, add_func, mul_func, zero_elem, I_elements)
    try:
        elements, add, mul, zero, I_elements = witness
        elements = list(elements)
        I_elements = list(I_elements)
        
        # H1: I is a proper ideal of R
        h1 = False
        if len(I_elements) < len(elements):
            is_ideal = True
            for a in I_elements:
                for b in I_elements:
                    if add(a, b) not in I_elements:
                        is_ideal = False
                for r in elements:
                    if mul(a, r) not in I_elements:
                        is_ideal = False
                    if mul(r, a) not in I_elements:
                        is_ideal = False
            h1 = is_ideal
            
        # H2: pi is the canonical projection (implicitly true for this representation)
        h2 = True
        
        # Helper to find all ideals in a finite ring using closure
        def find_ideals(ring_elements, r_add, r_mul, r_zero):
            def closure(generators):
                S = set(generators)
                S.add(r_zero)
                changed = True
                while changed:
                    changed = False
                    new_elems = set()
                    for a in S:
                        for b in S:
                            s = r_add(a, b)
                            if s not in S and s not in new_elems:
                                new_elems.add(s)
                        for r in ring_elements:
                            p1 = r_mul(a, r)
                            if p1 not in S and p1 not in new_elems:
                                new_elems.add(p1)
                            p2 = r_mul(r, a)
                            if p2 not in S and p2 not in new_elems:
                                new_elems.add(p2)
                    if new_elems:
                        S.update(new_elems)
                        changed = True
                return frozenset(S)
                
            current_ideals = {frozenset([r_zero])}
            all_ideals = set(current_ideals)
            
            for _ in range(len(ring_elements)):
                next_ideals = set()
                for I in current_ideals:
                    for x in ring_elements:
                        if x not in I:
                            new_gen = set(I)
                            new_gen.add(x)
                            J = closure(new_gen)
                            if J not in all_ideals:
                                next_ideals.add(J)
                if not next_ideals:
                    break
                all_ideals.update(next_ideals)
                current_ideals = next_ideals
                
            return list(all_ideals)

        ideals_R = find_ideals(elements, add, mul, zero)
        
        # Element-wise prime definition (completely prime)
        def is_elem_prime(P, r_elements, r_mul):
            if len(P) == len(r_elements):
                return False
            for a in r_elements:
                for b in r_elements:
                    if r_mul(a, b) in P:
                        if a not in P and b not in P:
                            return False
            return True

        # Ideal-wise prime definition (standard prime)
        def is_ideal_prime(P, ideals, r_elements, r_mul):
            if len(P) == len(r_elements):
                return False
            for A in ideals:
                for B in ideals:
                    ab_in_P = True
                    for a in A:
                        for b in B:
                            if r_mul(a, b) not in P:
                                ab_in_P = False
                                break
                        if not ab_in_P:
                            break
                    if ab_in_P:
                        if not (A.issubset(P) or B.issubset(P)):
                            return False
            return True

        # Quotient ring R/I
        cosets = []
        for a in elements:
            coset = frozenset([add(a, i) for i in I_elements])
            if coset not in cosets:
                cosets.append(coset)
                
        def q_add(C1, C2):
            a = next(iter(C1))
            b = next(iter(C2))
            return frozenset([add(add(a, b), i) for i in I_elements])
            
        def q_mul(C1, C2):
            a = next(iter(C1))
            b = next(iter(C2))
            return frozenset([add(mul(a, b), i) for i in I_elements])
            
        q_zero = frozenset(I_elements)
        
        ideals_Q = find_ideals(cosets, q_add, q_mul, q_zero)
        
        # Check bijection for element-wise prime
        prime_R_elem = [P for P in ideals_R if is_elem_prime(P, elements, mul)]
        prime_containing_I_elem = [P for P in prime_R_elem if frozenset(I_elements).issubset(P)]
        prime_Q_elem = [P for P in ideals_Q if is_elem_prime(P, cosets, q_mul)]
        bijection_elem = (len(prime_containing_I_elem) == len(prime_Q_elem))
        
        # Check bijection for ideal-wise prime
        prime_R_ideal = [P for P in ideals_R if is_ideal_prime(P, ideals_R, elements, mul)]
        prime_containing_I_ideal = [P for P in prime_R_ideal if frozenset(I_elements).issubset(P)]
        prime_Q_ideal = [P for P in ideals_Q if is_ideal_prime(P, ideals_Q, cosets, q_mul)]
        bijection_ideal = (len(prime_containing_I_ideal) == len(prime_Q_ideal))
        
        # If the bijection fails for either standard definition, the conclusion fails
        neg_q = not (bijection_elem and bijection_ideal)
        
        return [h1, h2, neg_q]
    except Exception:
        pass

    return [False, False, False]