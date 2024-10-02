def expanded_synthetic_division(dividend, divisor):
    """Fast polynomial division by using Expanded Synthetic Division.
    Also works with non-monic polynomials.

    Dividend and divisor are both polynomials, which are here simply lists of coefficients.
    E.g.: x**2 + 3*x + 5 will be represented as [1, 3, 5]
    """
    out = list(dividend)  # Copy the dividend
    normalizer = divisor[0]
    for i in range(len(dividend) - len(divisor) + 1):
        # For general polynomial division (when polynomials are non-monic),
        # we need to normalize by dividing the coefficient with the divisor's first coefficient
        out[i] /= normalizer

        coef = out[i]
        if coef != 0:  # Useless to multiply if coef is 0
            # In synthetic division, we always skip the first coefficient of the divisor,
            # because it is only used to normalize the dividend coefficients
            for j in range(1, len(divisor)):
                out[i + j] += -divisor[j] * coef

    # The resulting out contains both the quotient and the remainder,
    # the remainder being the size of the divisor (the remainder
    # has necessarily the same degree as the divisor since it is
    # what we couldn't divide from the dividend), so we compute the index
    # where this separation is, and return the quotient and remainder.
    separator = 1 - len(divisor)
    return out[:separator], out[separator:]  # Return quotient, remainder.


if __name__ == '__main__':
    print(expanded_synthetic_division([1, -2, -5, 6], [1, -3]))
