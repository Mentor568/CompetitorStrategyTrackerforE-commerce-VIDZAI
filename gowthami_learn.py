print("Hello")
print("Hello springboard!!!")
#x="hari"
x=str(4)
y=int(9.9)
d=float(8)
print(x,y,d)
print(type(x))
print(type(y))
print(type(d))
x = y = z = "Orange"
print(x)
print(y)
print(z)
fruits = ["a","b","c"]
x, y, z = fruits
print(x,y)
print(z)
x = "Python is awesome"
print(x)
print("It's alright")
print("He is called 'Johnny'")
print('He is called "Johnny"')
for x in "banana":
  print(x)
a = "Hello, World!"
print(len(a))
txt = "The best things in life are free!"
if "free" in txt:
  print("Yes, 'free' is present.")
b = "Hello, World!"
print(b[2:5])
a = "Hello, World!"
print(a.split(","))
this1 = ["apple", "banana", "cherry"]
print(len(this1))
thislist = ["apple", "banana", "cherry"]
for i in range(len(thislist)):
  print(thislist[i])
thislist = ["apple", "banana", "cherry"]
i = 0
while i < len(thislist):
  print(thislist[i])
  i = i + 1
list1 = ["a", "b" , "c"]
list2 = [1, 2, 3]
for x in list2:
  list1.append(x)
print(list1)
x=("apple","banana","cherry")
y=list(x)
y[1]="kiwi"
x=tuple(y)
print(x)
t= ("apple", "banana", "cherry")
y = list(t)
y.append("orange")
t= tuple(y)
print(t)
f= ("apple", "banana", "cherry")
mytuple = f* 2
print(mytuple)
thisdict = {
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}
print(thisdict["brand"])
for x,y in thisdict.items():
  print(x,y)
  
  
def is_prime(n):
    if n < 2:
        return False
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True
N = 10
print(f"Prime numbers between 1 and {N} are:")
for num in range(2, N + 1):
    if is_prime(num):  
        print(num, end=" ")
print()

#Maze solver problem

def is_valid_move(maze, x, y, visited):
    """Check if a move is valid (within bounds, not a wall, and not visited)."""
    return 0 <= x < len(maze) and 0 <= y < len(maze) and maze[x][y] == 0 and not visited[x][y]

def find_path_dfs(maze, x, y, visited, path):
    """Recursive DFS function to find a path in the maze."""
    # Base case: If we reach the exit
    if x == len(maze) - 1 and y == len(maze) - 1:
        path.append((x, y))
        return True
    
    # Mark current cell as visited
    visited[x][y] = True
    path.append((x, y))
    
    # Possible moves: Right, Down, Left, Up
    moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
    for dx, dy in moves:
        new_x, new_y = x + dx, y + dy
        if is_valid_move(maze, new_x, new_y, visited):
            if find_path_dfs(maze, new_x, new_y, visited, path):
                return True

    # Backtrack if no path found
    path.pop()
    return False

def solve_maze(maze):
    """Solves the maze using DFS and prints the path if found."""
    N = len(maze)
    visited = [[False] * N for _ in range(N)]
    path = []
    
    if find_path_dfs(maze, 0, 0, visited, path):
        print("Path found:")
        print(path)
    else:
        print("No path exists.")

# Example Maze (5x5 Grid)
maze = [
    [0, 1, 0, 0, 0],
    [0, 1, 0, 1, 0],
    [0, 0, 0, 1, 0],
    [1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0]
]

solve_maze(maze)

#bank loan calculator
def calculate_emi(principal, annual_rate, months):
    """Calculate EMI using the standard loan formula."""
    monthly_rate = annual_rate / 12 / 100  # Convert annual rate to monthly decimal
    emi = (principal * monthly_rate * (1 + monthly_rate) ** months) / ((1 + monthly_rate) ** months - 1)
    return round(emi, 2)

def generate_payment_schedule(principal, annual_rate, months):
    """Generate a detailed loan repayment schedule."""
    emi = calculate_emi(principal, annual_rate, months)
    remaining_balance = principal

    print(f"\nLoan Amount: {principal}, Interest Rate: {annual_rate}%, Tenure: {months} months")
    print(f"Monthly EMI: {emi}\n")
    print(f"{'Month':<8}{'EMI Paid':<12}{'Interest Paid':<15}{'Principal Paid':<15}{'Remaining Balance'}")

    for month in range(1, months + 1):
        interest = round((remaining_balance * (annual_rate / 12) / 100), 2)
        principal_paid = round(emi - interest, 2)
        remaining_balance = round(remaining_balance - principal_paid, 2)

        print(f"{month:<8}{emi:<12}{interest:<15}{principal_paid:<15}{remaining_balance}")

# Hardcoded Loan Details
principal_amount = 100000  # ₹100,000 loan amount
annual_interest_rate = 10  # 10% annual interest
loan_tenure_months = 12    # 12 months tenure

# Generate EMI and schedule
generate_payment_schedule(principal_amount, annual_interest_rate, loan_tenure_months)
