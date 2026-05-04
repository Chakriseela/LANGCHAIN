# Question 1
from functools import reduce

emp = [
    {"name": "Alice", "dept": "IT", "salary": "75000", "rating": 4.5, "active": True, "bonus": True},
    {"name": "Bob", "dept": "HR", "salary": "60000", "rating": 3.8, "active": True, "bonus": False},
    {"name": "Charlie", "dept": "IT", "salary": "not available", "rating": 4.9, "active": True, "bonus": True},
    {"name": "David", "dept": "Finance", "salary": "90000", "rating": 2.5, "active": False, "bonus": False},
    {"name": "Eva", "dept": "Finance", "salary": "85000", "rating": 4.2, "active": True, "bonus": True},
    {"name": "Frank", "dept": "HR", "salary": "62000", "rating": 4.0, "active": True, "bonus": True},
    {"name": "Grace", "dept": "IT", "salary": "98000", "rating": 4.7, "active": True, "bonus": True},
]

# 1️.Clean the data (fix salary)
def fix(e):
    try:
        e["salary"] = int(e["salary"])
    except:
        e["salary"] = 0
    return e

c1 = list(map(fix, emp))
print("Clean:", c1)

# 2️.Filter valid & active employees (salary > 0 and active)
f1 = list(filter(lambda x: x["active"] and x["salary"] > 0, c1))

# 3️.Transform salaries into yearly compensation
def yr(e):
    e["ys"] = e["salary"] * 12
    return e

c2 = list(map(yr, f1))
print("Filtered:", c2)

# 4️.Compute department-wise payroll
def dep(a, e):
    d = e["dept"]
    a[d] = a.get(d, 0) + e["ys"]
    return a

d1 = reduce(dep, c2, {})
print("Dept Pay:", d1)

# 5️.Find top-paid department
top = max(d1, key=d1.get)
print("Top Dept:", top)

# 6️.Calculate total bonus payout (10% of yearly salary if eligible)
def bonus(a, e):
    return a + (e["ys"] * 0.10 if e["bonus"] else 0)

b1 = reduce(bonus, c2, 0)
print("Bonus:", b1)

# 7️.Generate insightful statistics
cnt = len(c2)
avg = reduce(lambda a, e: a + e["ys"], c2, 0) / cnt
hp = list(filter(lambda x: x["rating"] >= 4.5, c2))

print("Avg:", avg)
print("High:", [x["name"] for x in hp])


# Question 2
import time

def retry(n, d):
    def dec(fn):
        def wrap(*a, **k):
            for i in range(n):
                try:
                    return fn(*a, **k)
                except:
                    print(f"Retry {i+1}")
                    if i == n - 1:
                        raise
                    time.sleep(d)
        return wrap
    return dec

@retry(3, 2)
def run():
    import random
    if random.random() < 0.8:
        raise Exception("Fail")
    return "OK"

print(run())

# *********************************************************

# Question 3–10
n1 = ["charan", "Bhanu", "jahnavi", "sana"]
u1 = [x.upper() for x in n1]
print("3:", u1)

w1 = ["apple", "banana", "cherry"]
f2 = [x[0] for x in w1]
print("4:", f2)

s1 = "Python is very powerful"
l1 = [len(x) for x in s1.split()]
print("5:", l1)

nums = [-5, 10, -2, 7, 0, 3]
p1 = [x for x in nums if x > 0]
print("6:", p1)

st = "hello world"
v1 = [x for x in st if x.lower() in "aeiou"]
print("7:", v1)

s2 = "This is a simple Python program"
l2 = [x for x in s2.split() if len(x) >= 4]
print("8:", l2)

w2 = ["python", "java", "code"]
r1 = [x[::-1] for x in w2]
print("9:", r1)

m1 = "Hello@123 World!!"
c3 = ''.join([x for x in m1 if x.isalnum()])
print("10:", c3)

# *********************************************************

# Question 11
stu = [("Alice", 78), ("Bob", 45), ("Charlie", 88), ("David", 60)]

# 1. students marks>= 50
p2 = list(filter(lambda x: x[1] >= 50, stu))
print(p2)
# 2. added 5 grace marks
g1 = list(map(lambda x: (x[0], x[1] + 5), p2))
print(g1)
# 3.srt by marks
srt = sorted(g1, key=lambda x: x[1], reverse=True)
print(srt)

# *********************************************************
# Object-oriented 
# Question 12
class Acc:
    def __init__(self, no, bal=0):
        self.no = no
        self.bal = bal

    def dep(self, amt):
        if amt > 0:
            self.bal += amt
            print("Dep:", amt)

    def wd(self, amt):
        if amt > self.bal:
            print("Low bal")
        else:
            self.bal -= amt
            print("Wd:", amt)

    def show(self):
        print(self.no, self.bal)

a = Acc("12345", 1000)
a.dep(500)
a.wd(300)
a.show()

# *********************************************************

# Question 13
class P:
    def __init__(self, n, a):
        self.n = n
        self.a = a

    def show(self):
        print(self.n, self.a)

class T(P):
    def __init__(self, n, a, sub, sal):
        super().__init__(n, a)
        self.sub = sub
        self.sal = sal

    def show(self):
        super().show()
        print(self.sub, self.sal)

t = T("Lakshmi", 30, "Math", 50000)
t.show()

# *********************************************************

# Question 14
import re

txt = """
Hello everyone! Today is 12-05-2024. Visit https://example.com or http://test.in.
Contact @support or use #Python #AI.
The price is 4500 and discount is 20%.
Another date is 25-12-2023.
"""
# Extract all numbers. 
print("Nums:", re.findall(r'\d+', txt))
# Extract all words starting with capital letters. 
print("Caps:", re.findall(r'\b[A-Z][a-z]*\b', txt))
# Extract all hashtags.
print("Tags:", re.findall(r'#\w+', txt))
# Extract all URLs. 
print("URLs:", re.findall(r'https?://\S+', txt))
# Extract all dates in DD-MM-YYYY format. 
print("Dates:", re.findall(r'\b\d{2}-\d{2}-\d{4}\b', txt))

# *********************************************************

# Question 15

# Remove extra spaces
s = "Python   is  a   very powerful   language"
print("Clean:", re.sub(r'\s+', ' ', s))

# Replace digits with *
u = "User123 has 45 new messages and 2 missed calls."
print("Mask:", re.sub(r'\d', '*', u))

# Mask credit card number (show only last 4 digits)
cc = "My credit card number is 4539 1488 0343 6467"
print("Card:", re.sub(r'\d(?=\d{4})', '*', cc.replace(" ", "")))

# Remove HTML tags
h = "<html><body><h1>Welcome</h1><p>This is <b>Python</b> Regex</p></body></html>"
print("HTML:", re.sub(r'<.*?>', '', h))

# Replace multiple punctuation with single one
p = "Wow!!! This is amazing... Really??? Yes!!!"
print("Punct:", re.sub(r'([.!?])\1+', r'\1', p)) 