def process_items():
    numbers = [3, 1, 2]

    # ruleid: python-in-place-mutation-none-assignment
    numbers = numbers.sort()

    words = ["a", "b"]
    # ruleid: python-in-place-mutation-none-assignment
    words = words.append("c")

    data = [1, 2]
    # ruleid: python-in-place-mutation-none-assignment
    data = data.reverse()

    # ok: python-in-place-mutation-none-assignment
    safe_numbers = [3, 1, 2]
    safe_numbers.sort()

    # ok: python-in-place-mutation-none-assignment
    sorted_copy = sorted(numbers or [])

    # ok: python-in-place-mutation-none-assignment
    safe_words = ["a", "b"]
    safe_words.append("c")
