def tee(iterable, n=2):
    iterator = iter(iterable)
    shared_link = [None, None]
    return tuple(_tee(iterator, shared_link) for _ in range(n))


def _tee(iterator, link):
    """Link is the same for every generator
    When while loop runs the link is change only
    for the generator that is run other generators
    are other instance with own scopes that refer
    to shared_link
    """
    try:
        while True:
            print(link)
            if link[1] is None:
                link[0] = next(iterator)
                link[1] = [None, None]
            value, link = link  # link[0], link[1] - link reassignment
            yield value
    # Expedition is raise what yielding is done
    except StopIteration:
        return


if __name__ == '__main__':
    gen1, gen2 = tee([1, 2, 3])

    print(id(gen1))
    print(id(gen2))

    print(next(gen1))  # Output: 1
    print(next(gen1))  # Output: 2
    print(next(gen1))  # Output: 3
    print(next(gen2))  # Output: 1
    print(next(gen2))  # Output: 2
    print(next(gen2))  # Output: 3

