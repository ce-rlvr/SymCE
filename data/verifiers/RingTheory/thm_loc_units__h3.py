import itertools

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness must provide:
      - R: a list of elements representing the ring
      - add: a function (x, y) -> z for addition in R
      - mul: a function (x, y) -> z for multiplication in R
      - S: a list of elements representing the multiplicatively closed subset
      - s: an element of S
      - a: an element of R
    """
    try:
        R = witness.R
        add = witness.add
        mul = witness.mul
        S = witness.S
        s = witness.s
        a = witness.a
    except AttributeError:
        return [False, False, False, False]

    # H1: R is a commutative ring
    h1_ok = True
    try:
        # Check closure, associativity, commutativity of add
        for x in R:
            for y in R:
                if add(x, y) not in R:
                    h1_ok = False
                if add(x, y) != add(y, x):
                    h1_ok = False
                for z in R:
                    if add(add(x, y), z) != add(x, add(y, z)):
                        h1_ok = False
        
        # Check zero element
        zeros = [z for z in R if all(add(x, z) == x for x in R)]
        if not zeros:
            h1_ok = False
            zero = None
        else:
            zero = zeros[0]
            
        # Check additive inverses
        if h1_ok:
            for x in R:
                if not any(add(x, y) == zero for y in R):
                    h1_ok = False
                    
        # Check closure, associativity, commutativity of mul
        for x in R:
            for y in R:
                if mul(x, y) not in R:
                    h1_ok = False
                if mul(x, y) != mul(y, x):
                    h1_ok = False
                for z in R:
                    if mul(mul(x, y), z) != mul(x, mul(y, z)):
                        h1_ok = False
                        
        # Check distributivity
        for x in R:
            for y in R:
                for z in R:
                    if mul(x, add(y, z)) != add(mul(x, y), mul(x, z)):
                        h1_ok = False
    except Exception:
        h1_ok = False

    # H2: S is a multiplicatively closed subset of R
    h2_ok = True
    try:
        if not all(x in R for x in S):
            h2_ok = False
        if not S:
            h2_ok = False
        for x in S:
            for y in S:
                if mul(x, y) not in S:
                    h2_ok = False
    except Exception:
        h2_ok = False

    # H3: s is an element of S
    h3_ok = True
    try:
        if s not in S:
            h3_ok = False
    except Exception:
        h3_ok = False

    # Conclusion: The fraction a/s is a unit in S^{-1}R if and only if there exists an element b in R such that ab is in S.
    # We evaluate the negation of the conclusion.
    neg_q_ok = False
    try:
        if not h1_ok or not h2_ok or not h3_ok:
            return [h1_ok, h2_ok, h3_ok, False]

        def neg(x):
            for y in R:
                if add(x, y) == zero:
                    return y
            return x
            
        # Check if there exists b in R such that ab in S
        exists_b = False
        for b in R:
            if mul(a, b) in S:
                exists_b = True
                break
                
        # Check if a/s is a unit in S^{-1}R
        # Two fractions x/y and z/w are equivalent if there exists u in S such that u(xw - yz) = 0
        def equiv(r1, t1, r2, t2):
            r1t2 = mul(r1, t2)
            r2t1 = mul(r2, t1)
            diff = add(r1t2, neg(r2t1))
            for u in S:
                if mul(u, diff) == zero:
                    return True
            return False

        # The identity element of S^{-1}R is e/e for any e in S. We can use s/s.
        # a/s is a unit if there exists c/t in S^{-1}R such that (a/s)(c/t) ~ s/s
        # i.e., ac/st ~ s/s
        is_unit = False
        for c in R:
            for t in S:
                ac = mul(a, c)
                st = mul(s, t)
                if equiv(ac, st, s, s):
                    is_unit = True
                    break
            if is_unit:
                break
                
        # The conclusion is the equivalence: is_unit <==> exists_b
        # The negation is that they are not equal
        neg_q_ok = (is_unit != exists_b)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: S is a multiplicatively closed subset of R",
    "H_3: s is an element of S",
    "¬Q: The equivalence (a/s is a unit iff exists b in R with ab in S) fails"
]

N_HYP = 3
NEG_Q_INDEX = 3