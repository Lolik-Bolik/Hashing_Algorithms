from algorithms import CuckooHashMap


def main():
    digits = [i for i in range(4)]
    hash_map_size = len(digits)
    h = CuckooHashMap(size=hash_map_size, elements_amount=len(digits))
    for digit in digits:
        h.insert(digit)
    print(h)
    # print(h.get_the_load_factor())
    # print(h.get(1))


if __name__ == "__main__":
    main()
