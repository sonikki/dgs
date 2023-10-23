import pandas as pd




def register(username, password):
    df = pd.read_csv(r'users.csv')
    if username in df['username'].values:
        print("Username already exists. Please choose a different one.")
    else:
        df = df._append({'username': username, 'password': password}, ignore_index=True)
        print("New DataFrame (after appending user):")
        print(df)  # Add this line for debugging
        df.to_csv('users.csv', index=False)
        print("Registration successful.")

def login(username, password):
    df = pd.read_csv('users.csv')
    user_row = df[df['username'] == username]
    if user_row.empty:
        print("User not found. Please register.")
    elif user_row['password'].values[0] == password:
        print("Login successful.")
    else:
        print("Incorrect password. Please try again.")

while True:
    print("1. Register")
    print("2. Login")
    print("3. Exit")
    choice = input("Enter your choice: ")

    if choice == '1':
        username = input("Enter username: ")
        password = input("Enter password: ")
        register(username, password)
    elif choice == '2':
        username = input("Enter username: ")
        password = input("Enter password: ")
        login(username, password)
    elif choice == '3':
        break
    else:
        print("Invalid choice. Please try again.")