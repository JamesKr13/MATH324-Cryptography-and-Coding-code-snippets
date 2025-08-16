def gcd_latex(a, b):
    """
    Computes gcd(a, b) using Euclid's algorithm and returns LaTeX code
    showing each step.
    """
    # Ensure a >= b
    if a < b:
        a, b = b, a

    steps = []
    x, y = a, b
    while y != 0:
        q = x // y
        r = x % y
        steps.append((x, y, q, r))
        x, y = y, r

    # Generate LaTeX code
    latex_code = "\\begin{align*}\n"
    for x, y, q, r in steps:
        latex_code += f"&{x} = {y} \\times {q} + {r} \\\\\n"
    latex_code += "\\end{align*}"

    return latex_code


def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a
