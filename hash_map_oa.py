# Author: Prince Emmanuel
# Description: Part 2, implement the HashMap class using open addressing.

from hm_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Takes a key and a value as parameters and updates the corresponding
        key/value pair in the hash map.
        """
        if self.table_load() >= 0.5:
            self.resize_table(self._capacity * 2)

        hash_val = self._hash_function(key)
        count = 0
        start_index = (hash_val + count ** 2) % self._capacity

        while True:
            if self._buckets[start_index] is None or \
                    self._buckets[start_index].is_tombstone is True:
                self._buckets[start_index] = HashEntry(key, value)
                self._size += 1
                break
            elif self._buckets[start_index].key == key:
                self._buckets[start_index].value = value
                break
            else:
                count += 1
                start_index = (hash_val + count ** 2) % self._capacity

    def table_load(self) -> float:
        """
        Takes no parameters and returns the current hash table load factor.
        """
        load_factor = self._size / self._capacity

        return load_factor

    def empty_buckets(self) -> int:
        """
        Takes no parameters and returns the number of empty buckets in
        the hash table.
        """
        count = 0

        for idx in range(self._capacity):
            if self._buckets[idx] is None or \
                    self._buckets[idx].is_tombstone is True:
                count += 1

        return count

    def resize_table(self, new_capacity: int) -> None:
        """
        Takes new_capacity as a parameter and changes the capacity of the
        internal hash table to new_capacity.
        """
        if new_capacity < self._size:
            return

        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        buckets_temp = self._buckets
        capacity_temp = self._capacity
        self.clear()
        new_buckets = DynamicArray()

        for _ in range(new_capacity):
            new_buckets.append(None)

        self._buckets = new_buckets
        self._size = 0
        self._capacity = new_capacity

        for idx in range(capacity_temp):
            if buckets_temp[idx] is not None and \
                    buckets_temp[idx].is_tombstone is False:
                bucket = buckets_temp[idx]
                self.put(bucket.key, bucket.value)

    def get(self, key: str) -> object:
        """
        Takes a key as a parameter and returns the value of the corresponding
        key in the hash map. None is returned if there is no match.
        """
        hash_val = self._hash_function(key)
        # count serves two purposes, aids in calculating the quadratic probing
        # formula and prevents infinite looping
        count = 0
        start_index = (hash_val + count ** 2) % self._capacity

        while count <= self._capacity:
            if self._buckets[start_index] is not None and \
                    self._buckets[start_index].key == key:
                if self._buckets[start_index].is_tombstone is False:
                    return self._buckets[start_index].value

            count += 1
            start_index = (hash_val + count ** 2) % self._capacity

    def contains_key(self, key: str) -> bool:
        """
        Take a key as a parameter and returns True if that key is in the hash
        map, otherwise it returns False.
        """
        contains = self.get(key)

        if contains is None:
            return False
        return True

    def remove(self, key: str) -> None:
        """
        Takes a key as a parameter and removes the corresponding key and its
        value from the hash map.
        """
        hash_val = self._hash_function(key)
        count = 0
        start_index = (hash_val + count ** 2) % self._capacity

        while count <= self._capacity:
            if self._buckets[start_index] is not None and \
                    self._buckets[start_index].key == key:
                if self._buckets[start_index].is_tombstone is False:
                    self._buckets[start_index].is_tombstone = True
                    self._size -= 1
                    break

            count += 1
            start_index = (hash_val + count ** 2) % self._capacity

    def clear(self) -> None:
        """
        Takes no parameters and clears the contents of the hash map.
        """
        temp = HashMap(self._capacity, self._hash_function)
        self._buckets = temp._buckets
        self._size = 0

    def get_keys_and_values(self) -> DynamicArray:
        """
        Takes no parameters and returns a dynamic array where each index
        contains a tuple of a key/value pair stored in the hash map.
        """
        hash_objects = DynamicArray()

        for idx in range(self._capacity):
            if self._buckets[idx] is not None and \
                    self._buckets[idx].is_tombstone is False:
                bucket = self._buckets[idx]
                hash_objects.append((bucket.key, bucket.value))

        return hash_objects

    def __iter__(self):
        """
        Takes no parameters and enables the hash map to iterate across itself.
        """
        self._index = 0

        return self

    def __next__(self):
        """
        Takes no parameters and returns the next item in the hash map, based on
        the current location of the iterator.
        """
        if self._buckets[self._index] is not None and \
                self._buckets[self._index].is_tombstone is False:
            value = self._buckets[self._index]
            self._index += 1
            return value
        else:
            raise StopIteration

# ------------------- BASIC TESTING ---------------------------------------- #


if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(23, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(11, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)
