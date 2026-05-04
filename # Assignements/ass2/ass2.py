#Question 1)
from functools import reduce

employees = [
    {"name": "Alice", "dept": "IT", "salary": "75000", "rating": 4.5, "active": True,  "bonus": True},
    {"name": "Bob", "dept": "HR", "salary": "60000", "rating": 3.8, "active": True,  "bonus": False},
    {"name": "Charlie", "dept": "IT", "salary": "not available", "rating": 4.9, "active": True,  "bonus": True},
    {"name": "David", "dept": "Finance", "salary": "90000", "rating": 2.5, "active": False, "bonus": False},
    {"name": "Eva", "dept": "Finance", "salary": "85000", "rating": 4.2, "active": True,  "bonus": True},
    {"name": "Frank", "dept": "HR", "salary": "62000", "rating": 4.0, "active": True,  "bonus": True},
    {"name": "Grace", "dept": "IT", "salary": "98000", "rating": 4.7, "active": True,  "bonus": True},
]

# 1️.Clean the data (fix salary)
def clean_data(emp):
    try:
        emp["salary"] = int(emp["salary"])
    except:
        emp["salary"] = 0
    return emp

cleaned_data = list(map(clean_data, employees))
print("Cleaned Data:\n", cleaned_data)


# 2️.Filter valid & active employees (salary > 0 and active)
filtered_data = list(filter(lambda e: e["active"] and e["salary"] > 0, cleaned_data))

# 3️.Transform salaries into yearly compensation
def yearly_salary(emp):
    emp["yearly_salary"] = emp["salary"] * 12
    return emp

yearly_data = list(map(yearly_salary, filtered_data))
print("\nFiltered Employees:\n", yearly_data)


# 4️.Compute department-wise payroll
def dept_payroll(acc, emp):
    dept = emp["dept"]
    acc[dept] = acc.get(dept, 0) + emp["yearly_salary"]
    return acc

dept_wise = reduce(dept_payroll, yearly_data, {})
print("\nDepartment-wise Payroll:\n", dept_wise)


# 5️.Find top-paid department
top_dept = max(dept_wise, key=dept_wise.get)
print("\nTop Paid Department:", top_dept)


# 6️.Calculate total bonus payout (10% of yearly salary if eligible)
def bonus_calc(acc, emp):
    if emp["bonus"]:
        acc += emp["yearly_salary"] * 0.10
    return acc

total_bonus = reduce(bonus_calc, yearly_data, 0)
print("\nTotal Bonus Payout:", total_bonus)


# 7️.Generate insightful statistics
total_employees = len(yearly_data)
avg_salary = reduce(lambda acc, e: acc + e["yearly_salary"], yearly_data, 0) / total_employees
high_performers = list(filter(lambda e: e["rating"] >= 4.5, yearly_data))
print("\nAverage Yearly Salary:", avg_salary)
print("\nHigh Performers:", [e["name"] for e in high_performers])


# ***************************************************************

# Question 2)
import time

def retry(max_attempts, delay):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for i in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    print(f"Retry {i+1}")
                    if i == max_attempts - 1:
                        raise
                    time.sleep(delay)
        return wrapper
    return decorator


@retry(3, 2)
def test():
    import random
    if random.random() < 0.8:
        raise Exception("Fail")
    return "Success"

print(test())

# ********************************************************
# List comprehension: 

#Question 3. Convert all names to uppercase
names_list = ["charan", "jahnavi", "sana"]
uppercase_names = [name.upper() for name in names_list]
print("3. Uppercase Names:", uppercase_names)


#Question 4. Extract the first letter from each word
words_list = ["apple", "banana", "cherry"]
first_letters_list = [word[0] for word in words_list]
print("4. First Letters:", first_letters_list)


#Question 5. Create a list of word lengths from a sentence
sentence_text = "Python is very powerful"
word_lengths = [len(word) for word in sentence_text.split()]
print("5. Word Lengths:", word_lengths)


#Question 6. Extract only positive numbers from a list
numbers_list = [-5, 10, -2, 7, 0, 3]
positive_numbers = [num for num in numbers_list if num > 0]
print("6. Positive Numbers:", positive_numbers)


#Question 7. Create a list containing only vowels from a string
input_string = "hello world"
vowel_list = [char for char in input_string if char.lower() in "aeiou"]
print("7. Vowels:", vowel_list)


#Question 8. Split sentence and remove words shorter than 4 characters
sentence_input = "This is a simple Python program"
long_words = [word for word in sentence_input.split() if len(word) >= 4]
print("8. Words (>=4 chars):", long_words)


#Question 9. Reverse each word in a list
original_words = ["python", "java", "code"]
reversed_words_list = [word[::-1] for word in original_words]
print("9. Reversed Words:", reversed_words_list)


#Question 10. Keep only alphanumeric characters from a string
mixed_string = "Hello@123 World!!"
clean_string = ''.join([char for char in mixed_string if char.isalnum()])
print("10. Alphanumeric Only:", clean_string)

# *************************************************************
# Lambda function 

#Question 11.)
students = [
    ("Alice", 78),
    ("Bob", 45),
    ("Charlie", 88),
    ("David", 60)
]
 
# 1. students marks>= 50
passed_students = list(filter(lambda s: s[1] >= 50, students))
print(passed_students)
# 2. added 5 grace marks
grace_marks = list(map(lambda s: (s[0], s[1] + 5), passed_students))
print(grace_marks)
# 3.srt by marks
sorted_students = sorted(grace_marks, key=lambda s: s[1], reverse=True)
print(sorted_students)

# ***********************************************************
# Object-oriented 

#Question 12.)
class BankAccount:
    def __init__(self, account_no, balance=0):
        self.account_no = account_no
        self.balance = balance
 
    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            print(f"Deposited: {amount}")
        else:
            print("Invalid deposit amount")
 
    def withdraw(self, amount):
        if amount > self.balance:
            print("Insufficient balance")
        elif amount <= 0:
            print("Invalid withdrawal amount")
        else:
            self.balance -= amount
            print(f"Withdrawn: {amount}")
 
    def show_balance(self):
        print(f"Account No: {self.account_no}, Balance: {self.balance}")
 
acc = BankAccount("12345", 1000)
acc.deposit(500)
acc.withdraw(300)
acc.show_balance()

# *****************************************************

#Question 13.)
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
 
    def display(self):
        print(f"Name: {self.name}")
        print(f"Age: {self.age}")
class Teacher(Person):
    def __init__(self, name, age, subject, salary):
        super().__init__(name, age)
        self.subject = subject
        self.salary = salary
    def display(self):
        super().display()  # call Person's display
        print(f"Subject: {self.subject}")
        print(f"Salary: {self.salary}")
t1 = Teacher("Lakshmi", 30, "Math", 50000)
t1.display()

# ***********************************************************
import re

#Question 14. Given a large text
text_data = """
Hello everyone! Today is 12-05-2024. Visit https://example.com or http://test.in.
Contact @support or use #Python #AI.
The price is 4500 and discount is 20%.
Another date is 25-12-2023.
"""

# Extract all numbers
numbers_list = re.findall(r'\d+', text_data)
print("Numbers:", numbers_list)

# Extract words starting with capital letters
capital_words = re.findall(r'\b[A-Z][a-z]*\b', text_data)
print("Capital Words:", capital_words)

# Extract hashtags
hashtags_list = re.findall(r'#\w+', text_data)
print("Hashtags:", hashtags_list)

# Extract URLs
urls_list = re.findall(r'https?://\S+', text_data)
print("URLs:", urls_list)

# Extract dates in DD-MM-YYYY format
dates_list = re.findall(r'\b\d{2}-\d{2}-\d{4}\b', text_data)
print("Dates:", dates_list)

# **************************************************************

#Question 15. Using regex

# Remove extra spaces
sentence_text = "Python   is  a   very powerful   language"
clean_sentence = re.sub(r'\s+', ' ', sentence_text)
print("\nClean Sentence:", clean_sentence)


# Replace digits with *
user_text = "User123 has 45 new messages and 2 missed calls."
masked_digits = re.sub(r'\d', '*', user_text)
print("Masked Digits:", masked_digits)


# Mask credit card number (show only last 4 digits)
card_text = "My credit card number is 4539 1488 0343 6467"
masked_card = re.sub(r'\d(?=\d{4})', '*', card_text.replace(" ", ""))
print("Masked Card:", masked_card)


# Remove HTML tags
html_text = "<html><body><h1>Welcome</h1><p>This is <b>Python</b> Regex</p></body></html>"
clean_html = re.sub(r'<.*?>', '', html_text)
print("Without HTML:", clean_html)


# Replace multiple punctuation with single one
punct_text = "Wow!!! This is amazing... Really??? Yes!!!"
clean_punct = re.sub(r'([.!?])\1+', r'\1', punct_text)
print("Clean Punctuation:", clean_punct)