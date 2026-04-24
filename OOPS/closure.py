# '''
# ✅ What is a Closure?
# A closure happens when:
# 1. You have an inner function.
# 2. The inner function uses variables from the outer function.
# 3. The outer function returns the inner function.
# 4. The returned function still remembers the outer function’s variables.
# 🔥 Simple Example of a Closure'''
# def N1():
#     def outer(x):
#         def inner():
#             return x
#         return inner

#     closure_func = outer(10)
#     print(closure_func())   # Output: 10
# # N1()


# '''⚡ Why Use Closures?
# ** Closures are useful for:
# ** Data hiding / encapsulation
# ** Maintaining state without using classes
# ** Creating function factories
# Decorators'''
# def N2():
#     def multiplier(n):
#         def multiply(x):
#             return x ** n
#         return multiply

#     double = multiplier(2)
#     triple = multiplier(3)

#     print(double(5))  # 10
#     print(triple(5))  # 15
#     print(double.__closure__)  
# # N2()


# '''🛡️ Closure with Hidden State (like private variables)'''
# def N3():
#     def Counter():
#         count = 0
#         def increment():
#             nonlocal count
#             count+=1
#             return count
#         return increment
    
#     c = Counter()
#     c1 = Counter()
#     print(c())
#     print(c())
#     print(c1())
# # N3()
# '''🧩 Important Keywords nonlocal
# Allows modifying variables from outer (but non-global) scope.'''


# '''🧊 Real-Life Example: Decorator
# Closures form the base of Python decorators:'''
# def N4():
#     def decorator(func):
#         def wrapper():
#             print("Before function")
#             func()
#             print("After function")
#         return wrapper
# N4()


# '''
# | Feature                         | Closure Benefit |
# | ------------------------------- | --------------- |
# | Remembers data                  | Yes             |
# | Works after outer function ends | Yes             |
# | Used in decorators              | Yes             |
# | Allows data hiding              | Yes             |
# | Needs nested function           | Yes             |
# '''

# '''
# 🔐 Why is this considered "private"?

# Because:

# ✔ No outside code can read or modify the variable
# ✔ Only the inner function can touch it
# ✔ Python does not provide a direct syntax to access cell variables

# This is similar to private variables in classes:
# self.__count  # private
# 🎯 Real Definition of Data Hiding in Closures

# A closure hides data by keeping variables in a private cell that only the inner function can access.
# They cannot be reached or modified directly from the outside environment.
# '''
# '''
# 🖼️ Visual Explanation
# counter()   ----->   count stored in hidden cell
#     |
#  returns increment() -----> can access & modify count
#                           (you cannot)
# 🧠 Why is this useful?
# ✔ Keeps state safe
# ✔ Prevents accidental modification
# ✔ Encapsulates logic — like private properties in OOP'''


# '''🔒 What Does “Hidden State” Mean in Closures?
# It means that:
# ✔ A variable exists
# ✔ The inner function can use it
# ❌ But you cannot access or modify that variable directly from outside.
# The variable is stored secretly inside the closure’s memory.
# 🧪 Let’s look at a simple closure again'''
# def N5():
#     def counter():
#         count = 0   # <---- private variable

#         def increment():
#             nonlocal count
#             count += 1
#             return count
        
#         return increment

#     c = counter()
#     print(c())  # 1
#     print(c())  # 2
#     print(c())  # 3
# N5()

# '''✔ increment() can read & modify count.
# ❌ What can’t we do?
# Try to access count directly:
# print(c.count)
# output::::
# AttributeError: 'function' object has no attribute 'count'

# ➡️ There is no way to access count from outside.
# This is data hiding.
# 🔍 Why can’t we access count?
# Because count is not an attribute of the returned function.
# It is stored in a hidden internal structure called a cell object, inside:
# c.__closure__

# Let’s see it:
# print(c.__closure__)  
# print(c.__closure__[0].cell_contents)

# Output:
# (<cell at 0x...: int object at ...>,)
# 0
# This proves:
# The outer variable is stored in a cell object
# Only the inner function has access to that cell
# '''

# '''
# ⚡ 4. Example Comparison: Counter with Closure vs Class
# Closure Version
# '''
# def counter():
#     count = 0
#     def inc():
#         nonlocal count
#         count += 1
#         return count
#     return inc

# c = counter()
# print(c())  # 1
# print(c())  # 2

# '''
# ✔ Minimal, clean
# ✔ Count truly hidden
# '''
# # Class Version
# class Counter:
#     def __init__(self):
#         self.__count = 0  # private-like

#     def inc(self):
#         self.__count += 1
#         return self.__count

# c = Counter()
# print(c.inc())  # 1
# print(c.inc())  # 2
# '''

import re
s = "ahad242 rfcd788 vdv347"
x = re.finditer(r"[a-z]{4}[0-9]{3}", s)
# print(next(x))


i = iter(range(5))
print(next(i))