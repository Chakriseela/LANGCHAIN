
# 1 Write a program to check if a number is even or odd.
def Que1():
    num = int(input("Enter number: "))
    if num % 2 == 0:
        print("Even")
    else:
        print("Odd")


# 2 Write a function to reverse a string.
def Que2():
    def reverse_string(s):
        return s[::-1]
    print(reverse_string("hello"))


# 3 Find the largest number in a list.
def Que3():
    nums = [10, 25, 5, 40]
    print(max(nums))


# 4 Calculate the factorial of a number using recursion.
def Que4():
    def factorial(n):
        if n == 0 or n == 1:
            return 1
        return n * factorial(n - 1)
    print(factorial(5))


# 5 Check if a string is a palindrome.
def Que5():
    def is_palindrome(s):
        return s == s[::-1]
    print(is_palindrome("madam"))


# 6 Count the number of vowels in a string.
def Que6():
    def count_vowels(s):
        vowels = "aeiouAEIOU"
        return sum(1 for char in s if char in vowels)
    print(count_vowels("hello world"))


# 7 Remove duplicates from a list.
def Que7():
    nums = [1, 2, 2, 3, 4, 4]
    unique = list(set(nums))
    print(unique)


# 8 Find the common elements in two lists.
def Que8():
    a = [1, 2, 3, 4]
    b = [3, 4, 5, 6]
    common = list(set(a) & set(b))
    print(common)


# 9 Merge two dictionaries into one.
def Que9():
    d1 = {"a": 1}
    d2 = {"b": 2}
    merged = {**d1, **d2}
    print(merged)


# 10 Sort a list of numbers.
def Que10():
    nums = [5, 2, 9, 1]
    nums.sort()
    print(nums)




# 11 Write a program to find the second largest number in a list.
def Que1_1():
    nums = [10, 20, 4, 45, 99]
    nums = list(set(nums))
    nums.sort()
    print(nums[-2])


# 12 Implement a function to flatten a nested list.
def Que1_2():
    def flatten(lst):
        result = []
        for i in lst:
            if isinstance(i, list):
                result.extend(flatten(i))
            else:
                result.append(i)
        return result
    print(flatten([1, [2, [3, 4], 5]]))


# 13 Perform a binary search on a sorted list.
def Que1_3():
    def binary_search(arr, target):
        left, right = 0, len(arr) - 1

        while left <= right:
            mid = (left + right) // 2

            if arr[mid] == target:
                return mid
            elif arr[mid] < target:
                left = mid + 1
            else:
                right = mid - 1

        return -1

    print(binary_search([1, 2, 3, 4, 5], 4))


# 14 Check if two strings are anagrams.
def Que1_4():
    def are_anagrams(s1, s2):
        return sorted(s1) == sorted(s2)
    print(are_anagrams("listen", "silent"))


# 15 Find the longest word in a sentence.
def Que1_5():
    def longest_word(sentence):
        words = sentence.split()
        return max(words, key=len)
    print(longest_word("I love programming in Python"))


# 16 Count the occurrences of each character in a string.
def Que1_6():
    def char_count(s):
        count = {}
        for char in s:
            count[char] = count.get(char, 0) + 1
        return count
    print(char_count("hello"))


# 17 Generate all permutations of a list.
def Que1_7():
    from itertools import permutations
    nums = [1, 2, 3]
    print(list(permutations(nums)))


# 18 Implement a stack using a list.
def Que1_8():
    stack = []

    # Push
    stack.append(1)
    stack.append(2)

    # Pop
    print(stack.pop())

    # Peek
    print(stack[-1])

    # Check if empty
    print(len(stack) == 0)




# Que1()
# Que2()
# Que3()
# Que4()
# Que5()
# Que6()
# Que7()
# Que8()
# Que9()
# Que10()
# Que1_1()
# Que1_2()
# Que1_3()
# Que1_4()
# Que1_5()
# Que1_6()
# Que1_7()
# Que1_8()