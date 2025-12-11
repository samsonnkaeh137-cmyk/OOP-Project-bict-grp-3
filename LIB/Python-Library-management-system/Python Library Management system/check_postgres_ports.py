"""
Check which PostgreSQL port is accessible with the given credentials.
"""
import psycopg2

user = "postgres"
password = "samson"
host = "localhost"

# Common ports for PostgreSQL
ports = [5432, 5433, 5434, 5435]

print("Checking PostgreSQL ports...")
print(f"User: {user}")
print(f"Password: {password}")
print(f"Host: {host}\n")

working_ports = []

for port in ports:
    try:
        print(f"Trying port {port}...", end=" ")
        conn = psycopg2.connect(
            dbname='postgres',
            user=user,
            password=password,
            host=host,
            port=port,
            connect_timeout=3
        )
        # Get PostgreSQL version
        cur = conn.cursor()
        cur.execute("SELECT version();")
        version = cur.fetchone()[0]
        cur.close()
        conn.close()
        print(f"✓ SUCCESS - {version.split(',')[0]}")
        working_ports.append(port)
    except psycopg2.OperationalError as e:
        if "password authentication" in str(e):
            print(f"✗ Password authentication failed")
        elif "Connection refused" in str(e) or "timeout" in str(e).lower():
            print(f"✗ Connection refused/timeout")
        else:
            print(f"✗ {str(e)[:50]}")
    except Exception as e:
        print(f"✗ Error: {str(e)[:50]}")

if working_ports:
    print(f"\n✓ Found working PostgreSQL on port(s): {working_ports}")
    print(f"\nUse port {working_ports[0]} in your configuration.")
else:
    print("\n✗ Could not connect to PostgreSQL on any port.")
    print("\nPlease check:")
    print("  1. PostgreSQL service is running")
    print("  2. Username and password are correct")
    print("  3. In pgAdmin4, check the server properties for the correct port")

