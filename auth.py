import bcrypt
import os
def hash_password(plain_text_password):
    # Encode the password to bytes, required by bcrypt
    password_bytes = plain_text_password.encode('utf-8')
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    # Decode the hash back to a string to store in a text file
    return hashed_password.decode('utf-8')
def verify_password(plain_text_password, hashed_password):
    # Encode both the plaintext password and stored hash to bytes
    password_bytes = plain_text_password.encode('utf-8')
    hashed_password_bytes = hashed_password.encode('utf-8')
    # bcrypt.checkpw handles extracting the salt and comparing
    return bcrypt.checkpw(password_bytes, hashed_password_bytes)
userdata='users.txt'
def register_user(username, password):
    hashed = hash_password(password)
    with open(userdata, 'a') as f:
        f.write(f"{username},{hashed}\n")
    print(f"User {username} registered successfully.")
def username_exists(username):
    if not os.path.exists(userdata):
        return False
    with open(userdata, 'r') as f:
        for line in f:
            stored_username, _ = line.strip().split(',')
            if stored_username == username:
                return True
    return False
def login_user(username, password): 
    if not os.path.exists(userdata):
        print("No users registered.")
        return False
    with open(userdata, 'r') as f:
        for line in f:
            stored_username, stored_hashed_password = line.strip().split(',')
            if stored_username == username:
                if verify_password(password, stored_hashed_password):
                    print(f"User {username} logged in successfully.")
                    return True
                else:
                    print("Incorrect password.")
                    return False
    print("Username not found.")
    return False
def validate_username(username):
    if len(username) < 3 or len(username) > 20:
        return False,'Username must be between 3 and 20 characters long.'
    if not username.isalnum():
        return False,'Username must be alphanumeric.'
    return True,''
def validate_password(password):
    if len(password) < 8:
        return False,'Password must be at least 8 characters long.'
    if not any(char.isdigit() for char in password):
        return False,'Password must contain at least one digit.'
    if not any(char.isupper() for char in password):
        return False,'Password must contain at least one uppercase letter.'
    if not any(char.islower() for char in password):
        return False,'Password must contain at least one lowercase letter.'
    return True,''
def display_menu():
    """Displays the main menu options."""
    print("\n" + "="*50)
    print(" MULTI-DOMAIN INTELLIGENCE PLATFORM")
    print(" Secure Authentication System")
    print("="*50)
    print("\n[1] Register a new user")
    print("[2] Login")
    print("[3] Exit")
    print("-"*50)
def main():
    """Main program loop."""
    print("\nWelcome to the Week 7 Authentication System!")

    while True:
        display_menu()
        choice = input("\nPlease select an option (1-3): ").strip()

        if choice == '1':
        # Registration flow
            print("\n--- USER REGISTRATION ---")
            username = input("Enter a username: ").strip()

            # Validate username
            is_valid, error_msg = validate_username(username)
            if not is_valid:
                print(f"Error: {error_msg}")
                continue
            if username_exists(username):
                print("Error: Username already exists.")
                continue

            password = input("Enter a password: ").strip()

            # Validate password
            is_valid, error_msg = validate_password(password)
            if not is_valid:
                print(f"Error: {error_msg}")
                continue

            # Confirm password
            password_confirm = input("Confirm password: ").strip()
            if password != password_confirm:
                print("Error: Passwords do not match.")
                continue

            # Register the user
            register_user(username, password)

        elif choice == '2':
            # Login flow
            print("\n--- USER LOGIN ---")
            username = input("Enter your username: ").strip()
            password = input("Enter your password: ").strip()

            # Attempt login
            if login_user(username, password):
                print("\nYou are now logged in.")

                # Optional: Ask if they want to logout or exit
                input("\nPress Enter to return to main menu...")

        elif choice == '3':
            # Exit
            print("\nThank you for using the authentication system.")
            print("Exiting...")
            break

        else:
            print("\nError: Invalid option. Please select 1, 2, or 3.")
if __name__ == "__main__":
    main()
