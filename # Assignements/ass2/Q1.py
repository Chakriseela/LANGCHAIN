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

# 1️⃣ Clean the data (fix salary)
def clean_data(emp):
    try:
        emp["salary"] = int(emp["salary"])
    except:
        emp["salary"] = 0
    return emp

cleaned_data = list(map(clean_data, employees))

# 2️⃣ Filter valid & active employees (salary > 0 and active)
filtered_data = list(filter(lambda e: e["active"] and e["salary"] > 0, cleaned_data))

# 3️⃣ Transform salaries into yearly compensation
def yearly_salary(emp):
    emp["yearly_salary"] = emp["salary"] * 12
    return emp

yearly_data = list(map(yearly_salary, filtered_data))

# 4️⃣ Compute department-wise payroll
def dept_payroll(acc, emp):
    dept = emp["dept"]
    acc[dept] = acc.get(dept, 0) + emp["yearly_salary"]
    return acc

dept_wise = reduce(dept_payroll, yearly_data, {})

# 5️⃣ Find top-paid department
top_dept = max(dept_wise, key=dept_wise.get)

# 6️⃣ Calculate total bonus payout (10% of yearly salary if eligible)
def bonus_calc(acc, emp):
    if emp["bonus"]:
        acc += emp["yearly_salary"] * 0.10
    return acc

total_bonus = reduce(bonus_calc, yearly_data, 0)

# 7️⃣ Generate insightful statistics
total_employees = len(yearly_data)
avg_salary = reduce(lambda acc, e: acc + e["yearly_salary"], yearly_data, 0) / total_employees
high_performers = list(filter(lambda e: e["rating"] >= 4.5, yearly_data))

# 📊 OUTPUT
print("Cleaned Data:\n", cleaned_data)
print("\nFiltered Employees:\n", yearly_data)
print("\nDepartment-wise Payroll:\n", dept_wise)
print("\nTop Paid Department:", top_dept)
print("\nTotal Bonus Payout:", total_bonus)
print("\nAverage Yearly Salary:", avg_salary)
print("\nHigh Performers:", [e["name"] for e in high_performers])