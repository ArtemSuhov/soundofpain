def numbers_to_bytes(data, bytes_for_one_number):
    result = bytearray()
    for num in data:
        temp = int(num)
        for b in range(bytes_for_one_number):
            result.append(temp % 256)
            temp = temp // 256
    return bytes(result)


def bytes_to_numbers(data, bytes_for_one_number):
    for i in range(0, len(data), bytes_for_one_number):
        yield sum(data[j] * (256 ** (j - i))
                  for j in range(i, i + bytes_for_one_number))
