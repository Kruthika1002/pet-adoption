import mysql.connector
from datetime import datetime

def connect_to_database():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Kruthi10",
        database="petadoption"
    )
    return mydb

def fetch_pets(db, search_term="", category=""):
    """Fetch all pets from the database, optionally filtering by search term and category."""
    cursor = db.cursor()
    query = "SELECT * FROM pets WHERE 1=1"
    params = []
    
    if search_term:
        query += " AND name LIKE %s"
        params.append('%' + search_term + '%')
    
    if category and category != "All":
        query += " AND category = %s"
        params.append(category)
    
    cursor.execute(query, tuple(params))
    pets = cursor.fetchall()
    cursor.close()
    return pets

def add_pet(connection, name, image_path, category, age, rescue_date, adoption_status):
    """Inserts a new pet into the database."""
    cursor = connection.cursor()
    query = "INSERT INTO pets (name, image_path, category, age, rescue_date, adoption_status) VALUES (%s, %s, %s, %s, %s, %s)"
    try:
        cursor.execute(query, (name, image_path, category, age, rescue_date, adoption_status))
        connection.commit()
        print("Pet added successfully.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()

def update_pet(mydb, pet_id, name, image_path, category, age, rescue_date, adoption_status):
    cursor = mydb.cursor()
    sql = """
        UPDATE pets 
        SET name = %s, image_path = %s, category = %s, 
            age = %s, rescue_date = %s, adoption_status = %s 
        WHERE id = %s
    """
    values = (name, image_path, category, age, rescue_date, adoption_status, pet_id)
    cursor.execute(sql, values)
    mydb.commit()
    cursor.close()

def delete_pet(connection, pet_id):
    """Deletes a pet from the database."""
    cursor = connection.cursor()
    query = "DELETE FROM pets WHERE id=%s"
    cursor.execute(query, (pet_id,))
    connection.commit()
    cursor.close()

def fetch_pet(connection, pet_id):
    """Fetches a single pet's details from the database."""
    cursor = connection.cursor()
    query = "SELECT * FROM pets WHERE id=%s"
    cursor.execute(query, (pet_id,))
    pet = cursor.fetchone()
    cursor.close()
    return pet

def fetch_pet_report(db):
    """Fetches total pets, count by category, and count by adoption status from the database."""
    cursor = db.cursor()
    
    # Get total number of pets
    cursor.execute("SELECT COUNT(*) FROM pets")
    total_pets = cursor.fetchone()[0]
    
    # Get number of pets by category
    cursor.execute("SELECT category, COUNT(*) FROM pets GROUP BY category")
    category_counts = cursor.fetchall()
    
    # Get number of pets by adoption status
    cursor.execute("SELECT adoption_status, COUNT(*) FROM pets GROUP BY adoption_status")
    adoption_status_counts = cursor.fetchall()
    
    cursor.close()
    return total_pets, category_counts, adoption_status_counts