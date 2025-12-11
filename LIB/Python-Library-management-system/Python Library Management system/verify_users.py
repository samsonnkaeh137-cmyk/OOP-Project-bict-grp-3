"""Verify that default users exist in the database."""
import os
os.environ['LIB_DB_NAME'] = 'library'
os.environ['LIB_DB_USER'] = 'postgres'
os.environ['LIB_DB_PASSWORD'] = 'samson'
os.environ['LIB_DB_HOST'] = 'localhost'
os.environ['LIB_DB_PORT'] = '5433'

from services.auth_service import AuthService

print("Checking default users...")
auth_service = AuthService()

# Test login for both users
users_to_test = [
    ("librarian", "admin123"),
    ("member", "member123")
]

print("\n" + "=" * 60)
print("USER VERIFICATION")
print("=" * 60)

for username, password in users_to_test:
    result = auth_service.login(username, password)
    if result:
        user_id, role_name = result
        print(f"✓ {username} - Role: {role_name} (ID: {user_id})")
    else:
        print(f"✗ {username} - Login FAILED")

print("=" * 60)
print("\nIf users are missing, they will be created automatically")
print("when you run the application.")

