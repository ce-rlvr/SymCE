import sympy
import sympy.combinatorics
import sympy.matrices
import math
import itertools

# Top-level setup
S3 = sympy.combinatorics.SymmetricGroup(3)
S4 = sympy.combinatorics.SymmetricGroup(4)
A4 = sympy.combinatorics.AlternatingGroup(4)
D4 = sympy.combinatorics.DihedralGroup(4)
C4 = sympy.combinatorics.CyclicGroup(4)
V4 = sympy.combinatorics.AlternatingGroup(4)
Z2 = sympy.combinatorics.CyclicGroup(2)
Z3 = sympy.combinatorics.CyclicGroup(3)
Z4 = sympy.combinatorics.CyclicGroup(4)
Z6 = sympy.combinatorics.CyclicGroup(6)
trivial = sympy.combinatorics.CyclicGroup(1)
I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness):
    # H_1: R is a ring
    try:
        if hasattr(witness, 'is_ring'):
            h1 = witness.is_ring()
        elif hasattr(witness, 'R'):
            h1 = hasattr(witness.R, 'is_Ring') and witness.R.is_Ring
            if not h1:
                h1 = witness.R == sympy.S.Integers or str(witness.R) in ['Z', 'ZZ', 'Integers']
        else:
            h1 = False
    except Exception:
        h1 = False

    # H_2: F is an arbitrary non-empty family of submodules of M
    try:
        if hasattr(witness, 'is_non_empty_family'):
            h2 = witness.is_non_empty_family()
        elif hasattr(witness, 'F'):
            if callable(witness.F):
                first_elem = witness.F(1)
            else:
                first_elem = next(iter(witness.F))
            h2 = first_elem is not None
        else:
            h2 = False
    except Exception:
        h2 = False

    # ¬Q: There is NO finite subset of F such that the intersection of the submodules 
    # in the finite subset is equal to the intersection of all submodules in F.
    try:
        if hasattr(witness, 'neg_q'):
            neg_q = witness.neg_q()
        elif hasattr(witness, 'check_neg_q'):
            neg_q = witness.check_neg_q()
        else:
            int_all = witness.intersection_all
            
            if callable(witness.F):
                elements = [witness.F(i) for i in range(1, 16)]
            else:
                if hasattr(witness.F, '__len__'):
                    # Finite family -> conclusion holds -> neg_Q is False
                    return [bool(h1), bool(h2), False]
                
                iterator = iter(witness.F)
                elements = list(itertools.islice(iterator, 15))
                try:
                    next_elem = next(iterator)
                    elements.append(next_elem)
                except StopIteration:
                    # Iterator exhausted, meaning the family is finite
                    return [bool(h1), bool(h2), False]
            
            # Check if strictly decreasing sequence of ideals in Z
            is_decreasing_Z = False
            try:
                is_decreasing_Z = True
                for i in range(len(elements)-1):
                    a = elements[i]
                    b = elements[i+1]
                    # In Z, ideal (a) strictly contains ideal (b) iff a divides b and |a| != |b|
                    if b % a != 0 or abs(b) == abs(a):
                        is_decreasing_Z = False
                        break
            except Exception:
                is_decreasing_Z = False
                
            is_decreasing_sets = False
            if not is_decreasing_Z:
                try:
                    is_decreasing_sets = True
                    for i in range(len(elements)-1):
                        a = elements[i]
                        b = elements[i+1]
                        if not b.is_subset(a) or b == a:
                            is_decreasing_sets = False
                            break
                except Exception:
                    is_decreasing_sets = False

            if is_decreasing_Z:
                if int_all == 0 and all(e != 0 for e in elements):
                    neg_q = True
                else:
                    neg_q = False
            elif is_decreasing_sets:
                if all(int_all.is_subset(e) and int_all != e for e in elements):
                    neg_q = True
                else:
                    neg_q = False
            else:
                # Fallback: check combinations of the sample
                neg_q = True
                for r in range(1, min(6, len(elements)+1)):
                    for subset in itertools.combinations(elements[:6], r):
                        if hasattr(subset[0], 'intersect'):
                            intersect = subset[0]
                            for elem in subset[1:]:
                                intersect = intersect.intersect(elem)
                            if intersect == int_all:
                                neg_q = False
                                break
                        else:
                            # Assume Z ideals (intersection is LCM)
                            lcm = subset[0]
                            for elem in subset[1:]:
                                lcm = abs(lcm * elem) // math.gcd(lcm, elem) if lcm and elem else 0
                            if lcm == int_all:
                                neg_q = False
                                break
                    if not neg_q:
                        break
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R is a ring",
    "H_2: F is an arbitrary non-empty family of submodules of M",
    "¬Q: No finite subset of F has an intersection equal to the intersection of all submodules in F"
]

N_HYP = 2
NEG_Q_INDEX = 2