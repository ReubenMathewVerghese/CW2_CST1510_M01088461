import bcrypt
import os
def hash_password(plain_text_password):
    """
    Hash a plaintext password for secure storage.
    """
    # Encode the password to bytes, required by bcrypt
    password_bytes = plain_text_password.encode('utf-8')
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    # Decode the hash back to a string to store in a text file
    return hashed_password.decode('utf-8')

def verify_password(plain_text_password, hashed_password):
    """
    Verify a plaintext password against the stored hashed password.
    """
    # Encode both the plaintext password and stored hash to bytes
    password_bytes = plain_text_password.encode('utf-8')
    hashed_password_bytes = hashed_password.encode('utf-8')
    # bcrypt.checkpw handles extracting the salt and comparing
    if bcrypt.checkpw(password_bytes, hashed_password_bytes):
        return True
    
    return False

def register_user(username, password):
    """
    Register a new user by storing their username and hashed password in a text file.
    """
    hashed_password = hash_password(password)
    userdata = 'users.txt'
    
    # Check if username already exists
    if username_exists(username):
        print(f"Error: Username '{username}' already exists.")
        return False
    
    # Append the new user to the file
    with open(userdata, 'a') as f:
        f.write(f"{username},{hashed_password}\n")
    
    print(f"User '{username}' registered successfully.")
    return True

def username_exists(username):
    """
    Check if a username already exists in the userdata file.
    """
    userdata = 'users.txt'
    if not os.path.exists(userdata):
        return False
    with open(userdata, 'r') as f:
        for line in f:
            stored_username, _ = line.strip().split(',')
            if stored_username == username:
                return True
    return False

def login_user(username, password): 
    """
    Authenticate a user by verifying their username and password.
    """
    userdata = 'users.txt'
    if not os.path.exists(userdata):
        print("Error: No users registered yet.")
        return False
    
    with open(userdata, 'r') as f:
        for line in f:
            stored_username, stored_hashed_password = line.strip().split(',')
            if stored_username == username:
                if verify_password(password, stored_hashed_password):
                    print(f"Login successful! Welcome, {username}.")
                    return True
                else:
                    print("Error: Incorrect password.")
                    return False
    
    print("Error: User not found.")
    return False

def validate_username(username):
    if len(username) < 3 or len(username) > 20:
        return False,'Username must be between 3 and 20 characters long.'
    if not username.isalnum():
        return False,'Username must be alphanumeric.'
    return True,''

def validate_password(passWd: str, confPWrd: str) -> tuple:
    """
    Validates passWd using various criteria
    Returns: Tuple (bool, string) -> (IsValid, ErrorMessage)
    """
    errorMsg = ""
    validated = True

    # 1. Check Length
    if not (6 <= len(passWd) <= 50):
        validated = False
        errorMsg += "Length should be between 6 and 50 characters.\n"

    # 2. Check Special Characters
    if "_" not in passWd and "@" not in passWd:
        validated = False
        errorMsg += "Must contain special characters (@ or _).\n"

    # 3. Check Matching Passwords
    if passWd != confPWrd:
        validated = False
        errorMsg += "Passwords do not match.\n"

    return (validated, errorMsg)

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
            password_confirm = input("Confirm password: ").strip()

            is_valid, error_msg = validate_password(password, password_confirm)
            
            if not is_valid:
                print(f"Error: {error_msg}")
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
