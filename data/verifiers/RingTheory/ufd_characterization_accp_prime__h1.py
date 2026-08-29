import sympy
from sympy import ZZ, QQ
from sympy.abc import x, y, z

def conditions(witness):
    try:
        if witness == ZZ or witness == QQ:
            return [False]
    except Exception:
        pass

    n = None
    if isinstance(witness, str):
        import re
        m = re.match(r'Z/(\d+)Z', witness.replace(' ', ''))
        if m:
            n = int(m.group(1))
        else:
            try:
                n = int(witness)
            except Exception:
                pass
    else:
        try:
            n = int(witness)
        except Exception:
            pass

    if n is None or n < 2:
        return [False]

    try:
        # In a finite ring Z/nZ, it is a UFD if and only if it is a field (n is prime).
        is_ufd = sympy.isprime(n)
        
        # Find units in Z/nZ
        units = set(i for i in range(1, n) if sympy.gcd(i, n) == 1)
        non_units = [i for i in range(n) if i not in units]
        
        # Find elements that can be factored into two non-units
        reducible_elements = set()
        for b in non_units:
            for c in non_units:
                reducible_elements.add((b * c) % n)
                
        # Irreducible elements are non-zero, non-units that cannot be factored into two non-units
        irreducibles = set()
        for a in range(1, n):
            if a not in units and a not in reducible_elements:
                irreducibles.add(a)
                
        # Check if every irreducible is prime
        # p is prime if p|ab implies p|a or p|b
        all_prime = True
        for p in irreducibles:
            multiples = set((p * k) % n for k in range(n))
            is_prime = True
            non_multiples = [val for val in range(n) if val not in multiples]
            
            for a in non_multiples:
                for b in non_multiples:
                    if (a * b) % n in multiples:
                        is_prime = False
                        break
                if not is_prime:
                    break
            
            if not is_prime:
                all_prime = False
                break
                
        # Finite rings always satisfy the Ascending Chain Condition on Principal ideals (ACCP)
        accp = True
        
        rhs = accp and all_prime
        
        # The conclusion is the equivalence: R is a UFD iff (ACCP and every irreducible is prime)
        # We want the negation of this conclusion (i.e., the equivalence fails)
        neg_q = (is_ufd != rhs)
        
        return [neg_q]
    except Exception:
        return [False]

CONDITION_LABELS = [
    "¬Q: The equivalence 'R is a UFD iff R satisfies ACCP and every irreducible is prime' fails"
]

N_HYP = 0
NEG_Q_INDEX = 0