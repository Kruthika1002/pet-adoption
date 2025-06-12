import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import ImageTk, Image
import database
from datetime import datetime
from tkcalendar import DateEntry

def connect_to_database():
    """Connects to the MySQL database using credentials."""
    return database.connect_to_database()

def fetch_pets(search_term="", category=""):
    """Retrieves pet data from the database based on search criteria."""
    mydb = connect_to_database()
    pets = database.fetch_pets(mydb, search_term, category)
    mydb.close()
    return pets

def display_pets(pets):
    """Displays pet information in frames with images, names, and details."""
    for widget in pet_list_frame.winfo_children():
        widget.destroy()
        
    for pet in pets:
        frame = tk.Frame(pet_list_frame, bg="#f0f8ff")#image and update and delete buttons
        frame.pack(pady=10, fill=tk.X, padx=10)

        try:
            img = Image.open(pet[2])
            img = img.resize((100, 100))
            img = ImageTk.PhotoImage(img)
            panel = tk.Label(frame, image=img)
            panel.image = img
            panel.pack(side=tk.LEFT)

            info_frame = tk.Frame(frame, bg="#f0f8ff")# space after details of pet
            info_frame.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)

            name_label = tk.Label(info_frame, text=f"Name: {pet[1]}", bg="#f0f8ff", font=("Helvetica", 12))# colour behind text name
            name_label.pack(anchor="w")

            category_label = tk.Label(info_frame, text=f"Category: {pet[3]}", bg="#f0f8ff", font=("Helvetica", 12))# colour behind category
            category_label.pack(anchor="w")

            age_label = tk.Label(info_frame, text=f"Age: {pet[4]}", bg="#f0f8ff", font=("Helvetica", 12))# colour behind age
            age_label.pack(anchor="w")

            rescue_date_label = tk.Label(info_frame, text=f"Rescue Date: {pet[5]}", bg="#f0f8ff", font=("Helvetica", 12))# colour behind rescue date
            rescue_date_label.pack(anchor="w")

            status_label = tk.Label(info_frame, text=f"Status: {pet[6]}", bg="#f0f8ff", font=("Helvetica", 12))# colour behind status
            status_label.pack(anchor="w")

            # Buttons frame
            button_frame = tk.Frame(frame, bg="#f0f8ff")# right side of update and delete buttons
            button_frame.pack(side=tk.RIGHT, padx=10)

            update_button = tk.Button(
                button_frame, 
                text="Update", 
                command=lambda p=pet[0]: update_pet(p),
                bg="#90ee90",
                font=("Helvetica", 10)
            )
            update_button.pack(side=tk.LEFT, padx=5)

            delete_button = tk.Button(
                button_frame, 
                text="Delete", 
                command=lambda p=pet[0]: delete_pet(p),
                bg="#ffcccb",
                font=("Helvetica", 10)
            )
            delete_button.pack(side=tk.LEFT)

        except Exception as e:
            messagebox.showerror("Error", f"Error displaying pet: {str(e)}")

def refresh_pet_list():
    """Refreshes the pet list based on search criteria."""
    pets = fetch_pets(search_term.get(), category_var.get())
    display_pets(pets)

def delete_pet(pet_id):
    """Confirms deletion with user and calls the database function to remove the pet."""
    confirmation = messagebox.askquestion("Delete Pet", "Are you sure you want to delete this pet?")
    if confirmation == "yes":
        database.delete_pet(connect_to_database(), pet_id)
        refresh_pet_list()
        
def add_pet():
    """Opens a dialog to collect new pet information and inserts it into the database."""
    add_pet_window = tk.Toplevel(root)
    add_pet_window.title("Add Pet")
    add_pet_window.config(bg="#f0f8ff")  # Light blue background
    add_pet_window.geometry("500x650")

    # Name
    name_label = tk.Label(add_pet_window, text="Name:", bg="#f0f8ff", font=("Helvetica", 12))
    name_label.pack(pady=5)
    name_entry = tk.Entry(add_pet_window, font=("Helvetica", 12))
    name_entry.pack(pady=5)

    # Image Path
    image_path_label = tk.Label(add_pet_window, text="Image Path:", bg="#f0f8ff", font=("Helvetica", 12))
    image_path_label.pack(pady=5)
    image_path_entry = tk.Entry(add_pet_window, font=("Helvetica", 12))
    image_path_entry.pack(pady=5)

    def browse_image():
        """Opens a file dialog to select an image file and refocuses on the add_pet_window."""
        file_path = filedialog.askopenfilename(
            title="Select an Image", 
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif")]
        )
        if file_path:  # Check if a file was selected
            image_path_entry.delete(0, tk.END)  # Clear the entry
            image_path_entry.insert(0, file_path)  # Insert the selected file path
            add_pet_window.focus_force()  # Refocus on add_pet_window

    browse_button = tk.Button(add_pet_window, text="Browse", command=browse_image, bg="#90ee90", font=("Helvetica", 12))
    browse_button.pack(pady=5)

    # Category
    category_label = tk.Label(add_pet_window, text="Category:", bg="#f0f8ff", font=("Helvetica", 12))
    category_label.pack(pady=5)
    category_entry = tk.Entry(add_pet_window, font=("Helvetica", 12))
    category_entry.pack(pady=5)

    # Age
    age_label = tk.Label(add_pet_window, text="Age:", bg="#f0f8ff", font=("Helvetica", 12))
    age_label.pack(pady=5)
    age_entry = tk.Entry(add_pet_window, font=("Helvetica", 12))
    age_entry.pack(pady=5)

    # Rescue Date
    rescue_date_label = tk.Label(add_pet_window, text="Rescue Date:", bg="#f0f8ff", font=("Helvetica", 12))
    rescue_date_label.pack(pady=5)
    rescue_date_entry = DateEntry(add_pet_window, width=12, background='darkblue', foreground='white', borderwidth=2)
    rescue_date_entry.pack(pady=5)

    # Adoption Status
    status_label = tk.Label(add_pet_window, text="Adoption Status:", bg="#f0f8ff", font=("Helvetica", 12))
    status_label.pack(pady=5)
    status_var = tk.StringVar(value="Available")
    status_options = ["Available", "Adopted", "Pending"]
    status_menu = tk.OptionMenu(add_pet_window, status_var, *status_options)
    status_menu.config(font=("Helvetica", 12))
    status_menu.pack(pady=5)

    def submit_add_pet():
        """Collects user input and calls the database function to insert a new pet."""
        name = name_entry.get().strip()
        image_path = image_path_entry.get().strip()
        category = category_entry.get().strip()

        try:
            age = int(age_entry.get().strip())
        except ValueError:
            messagebox.showerror("Input Error", "Age must be a number.")
            return

        rescue_date = rescue_date_entry.get_date()
        adoption_status = status_var.get()

        if not all([name, image_path, category, age, rescue_date, adoption_status]):
            messagebox.showerror("Input Error", "All fields must be filled out.")
            return

        database.add_pet(connect_to_database(), name, image_path, category, age, rescue_date, adoption_status)
        add_pet_window.destroy()  # Close the dialog window after adding the pet
        refresh_pet_list()  # Update the pet list on the main window

    submit_button = tk.Button(add_pet_window, text="Add Pet", command=submit_add_pet, bg="#add8e6", font=("Helvetica", 12))
    submit_button.pack(pady=5)

def update_pet(pet_id):
    """Opens a dialog to update existing pet information."""
    mydb = connect_to_database()
    pet = database.fetch_pet(mydb, pet_id)
    mydb.close()
    
    if pet is None:
        messagebox.showerror("Fetch Error", "Could not fetch pet details.")
        return

    update_pet_window = tk.Toplevel(root)
    update_pet_window.title("Update Pet")
    update_pet_window.config(bg="#f0f8ff")
    update_pet_window.geometry("500x700")

    # Name
    name_label = tk.Label(update_pet_window, text="Name:", bg="#f0f8ff", font=("Helvetica", 12))
    name_label.pack(pady=5)
    name_entry = tk.Entry(update_pet_window, font=("Helvetica", 12))
    name_entry.insert(0, pet[1])  # Insert current name
    name_entry.pack(pady=5)

    # Image Path
    image_path_label = tk.Label(update_pet_window, text="Image Path:", bg="#f0f8ff", font=("Helvetica", 12))
    image_path_label.pack(pady=5)
    image_path_entry = tk.Entry(update_pet_window, font=("Helvetica", 12))
    image_path_entry.insert(0, pet[2])  # Insert current image path
    image_path_entry.pack(pady=5)

    def browse_image():
        file_path = filedialog.askopenfilename(
            title="Select an Image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif")]
        )
        if file_path:
            image_path_entry.delete(0, tk.END)
            image_path_entry.insert(0, file_path)

    browse_button = tk.Button(
        update_pet_window, 
        text="Browse", 
        command=browse_image, 
        bg="#90ee90", 
        font=("Helvetica", 12)
    )
    browse_button.pack(pady=5)

    # Show current image preview
    try:
        img = Image.open(pet[2])
        img = img.resize((100, 100))
        img = ImageTk.PhotoImage(img)
        image_preview = tk.Label(update_pet_window, image=img, bg="#f0f8ff")
        image_preview.image = img
        image_preview.pack(pady=5)
    except Exception as e:
        image_preview = tk.Label(update_pet_window, text="No image available", bg="#f0f8ff", font=("Helvetica", 10))
        image_preview.pack(pady=5)

    # Category
    category_label = tk.Label(update_pet_window, text="Category:", bg="#f0f8ff", font=("Helvetica", 12))
    category_label.pack(pady=5)
    category_var = tk.StringVar(value=pet[3])  # Set current category
    category_options = ["Dog", "Cat", "Bird", "Other"]
    category_menu = tk.OptionMenu(update_pet_window, category_var, *category_options)
    category_menu.config(font=("Helvetica", 12))
    category_menu.pack(pady=5)

    # Age
    age_label = tk.Label(update_pet_window, text="Age:", bg="#f0f8ff", font=("Helvetica", 12))
    age_label.pack(pady=5)
    age_entry = tk.Entry(update_pet_window, font=("Helvetica", 12))
    age_entry.insert(0, str(pet[4]))  # Insert current age
    age_entry.pack(pady=5)

    # Rescue Date
    rescue_date_label = tk.Label(update_pet_window, text="Rescue Date:", bg="#f0f8ff", font=("Helvetica", 12))
    rescue_date_label.pack(pady=5)
    rescue_date_entry = DateEntry(update_pet_window, width=12, background='darkblue', foreground='white', borderwidth=2)
    rescue_date_entry.set_date(pet[5])  # Set current rescue date
    rescue_date_entry.pack(pady=5)

    # Adoption Status
    status_label = tk.Label(update_pet_window, text="Adoption Status:", bg="#f0f8ff", font=("Helvetica", 12))
    status_label.pack(pady=5)
    status_var = tk.StringVar(value=pet[6])  # Set current status
    status_options = ["Available", "Adopted", "Pending"]
    status_menu = tk.OptionMenu(update_pet_window, status_var, *status_options)
    status_menu.config(font=("Helvetica", 12))
    status_menu.pack(pady=5)

    def submit_update():
        """Validates and submits the updated pet information."""
        try:
            # Collect updated values
            name = name_entry.get().strip()
            image_path = image_path_entry.get().strip()
            category = category_var.get()
            
            try:
                age = int(age_entry.get().strip())
            except ValueError:
                messagebox.showerror("Input Error", "Age must be a number.")
                return

            rescue_date = rescue_date_entry.get_date()
            adoption_status = status_var.get()

            # Validate inputs
            if not all([name, image_path, category, age, rescue_date, adoption_status]):
                messagebox.showerror("Input Error", "All fields must be filled out.")
                return

            # Update in database
            mydb = connect_to_database()
            database.update_pet(
                mydb,
                pet_id,
                name,
                image_path,
                category,
                age,
                rescue_date,
                adoption_status
            )
            mydb.close()

            messagebox.showinfo("Success", "Pet information updated successfully!")
            update_pet_window.destroy()
            refresh_pet_list()  # Refresh the main window's pet list

        except Exception as e:
            messagebox.showerror("Error", f"Failed to update pet: {str(e)}")

    # Submit button
    submit_button = tk.Button(
        update_pet_window,
        text="Update Pet",
        command=submit_update,
        bg="#add8e6",
        font=("Helvetica", 12)
    )
    submit_button.pack(pady=20)

    # Cancel button
    cancel_button = tk.Button(
        update_pet_window,
        text="Cancel",
        command=update_pet_window.destroy,
        bg="#ffcccb",
        font=("Helvetica", 12)
    )
    cancel_button.pack(pady=5)

def generate_report():
    """Generates a report of total pets, pets by category, and pets by adoption status."""
    mydb = connect_to_database()
    if not mydb:
        messagebox.showerror("Database Error", "Could not connect to the database.")
        return
    
    # Fetch report data
    try:
        total_pets, category_counts, adoption_status_counts = database.fetch_pet_report(mydb)
    except Exception as e:
        messagebox.showerror("Database Error", f"Error fetching report data: {e}")
        return
    finally:
        mydb.close()

    # Create a new window for the report
    report_window = tk.Toplevel(root)
    report_window.title("Pet Report")
    report_window.config(bg="#f0f8ff", padx=20, pady=20)

    # Title
    report_label = tk.Label(report_window, text="Pet Report", bg="#f0f8ff", font=("Helvetica", 18, "bold"))
    report_label.pack(pady=(0, 15))

    # Total Pets
    total_frame = tk.Frame(report_window, bg="#e6f7ff", bd=2, relief="groove", padx=10, pady=10)
    total_frame.pack(fill="x", pady=(0, 10))
    total_label = tk.Label(total_frame, text=f"Total Number of Pets: {total_pets}", bg="#e6f7ff", font=("Helvetica", 14, "bold"))
    total_label.pack()

    # Pets by Category Section
    category_frame = tk.Frame(report_window, bg="#d9f2e6", bd=2, relief="groove", padx=10, pady=10)
    category_frame.pack(fill="x", pady=(0, 10))
    category_label = tk.Label(category_frame, text="Pets by Category", bg="#d9f2e6", font=("Helvetica", 14, "bold"))
    category_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))

    # Table Headers for Category
    header_font = ("Helvetica", 12, "bold")
    tk.Label(category_frame, text="Category", bg="#d9f2e6", font=header_font).grid(row=1, column=0, padx=5, pady=5, sticky="w")
    tk.Label(category_frame, text="Count", bg="#d9f2e6", font=header_font).grid(row=1, column=1, padx=5, pady=5, sticky="w")

    # Category Data
    for i, (category, count) in enumerate(category_counts, start=2):
        bg_color = "#f0fff0" if i % 2 == 0 else "#e6f7ff"
        tk.Label(category_frame, text=category, bg=bg_color, font=("Helvetica", 12)).grid(row=i, column=0, padx=5, pady=3, sticky="w")
        tk.Label(category_frame, text=count, bg=bg_color, font=("Helvetica", 12)).grid(row=i, column=1, padx=5, pady=3, sticky="w")

    # Pets by Adoption Status Section
    status_frame = tk.Frame(report_window, bg="#f2e6ff", bd=2, relief="groove", padx=10, pady=10)
    status_frame.pack(fill="x", pady=(0, 10))
    status_label = tk.Label(status_frame, text="Pets by Adoption Status", bg="#f2e6ff", font=("Helvetica", 14, "bold"))
    status_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))

    # Table Headers for Adoption Status
    tk.Label(status_frame, text="Adoption Status", bg="#f2e6ff", font=header_font).grid(row=1, column=0, padx=5, pady=5, sticky="w")
    tk.Label(status_frame, text="Count", bg="#f2e6ff", font=header_font).grid(row=1, column=1, padx=5, pady=5, sticky="w")

    # Adoption Status Data
    for i, (adoption_status, count) in enumerate(adoption_status_counts, start=2):
        bg_color = "#f9f0ff" if i % 2 == 0 else "#e6f7ff"
        tk.Label(status_frame, text=adoption_status, bg=bg_color, font=("Helvetica", 12)).grid(row=i, column=0, padx=5, pady=3, sticky="w")
        tk.Label(status_frame, text=count, bg=bg_color, font=("Helvetica", 12)).grid(row=i, column=1, padx=5, pady=3, sticky="w")






# Create main window
root = tk.Tk()
root.title("Pet Management System")
root.geometry("800x600")
root.config(bg="#f0f8ff")# behind the actual window

# Assuming there's a button to generate the report
generate_report_button = tk.Button(root, text="Generate Report", command=generate_report)
generate_report_button.pack()

# Create main container
main_container = tk.Frame(root, bg="#f0f8ff")#top of list of pets
main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

# Search and filter section
search_frame = tk.Frame(main_container, bg="#f0f8ff")#inbetween search category and add pet button
search_frame.pack(fill=tk.X, pady=10)

# Search entry
search_label = tk.Label(search_frame, text="Search by name:", bg="#f0f8ff", font=("Helvetica", 12))
search_label.pack(side=tk.LEFT, padx=5)

search_term = tk.StringVar()
search_entry = tk.Entry(search_frame, textvariable=search_term, font=("Helvetica", 12))
search_entry.pack(side=tk.LEFT, padx=5)

# Category filter
category_label = tk.Label(search_frame, text="Category:", bg="#f0f8ff", font=("Helvetica", 12))
category_label.pack(side=tk.LEFT, padx=5)

category_var = tk.StringVar(value="")
category_options = ["All", "Dog", "Cat", "Bird", "Other"]
category_menu = tk.OptionMenu(search_frame, category_var, *category_options)
category_menu.config(font=("Helvetica", 12))
category_menu.pack(side=tk.LEFT, padx=5)

# Search button
search_button = tk.Button(
    search_frame,
    text="Search",
    command=refresh_pet_list,
    bg="#add8e6",
    font=("Helvetica", 12)
)
search_button.pack(side=tk.LEFT, padx=5)

# Add pet button
add_pet_button = tk.Button(
    search_frame,
    text="Add Pet",
    command=add_pet,
    bg="#90ee90",
    font=("Helvetica", 12)
)
add_pet_button.pack(side=tk.RIGHT, padx=5)

# Create scrollable frame for pet list
canvas = tk.Canvas(main_container, bg="#f0f8ff") # behind list of pets
scrollbar = tk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
pet_list_frame = tk.Frame(canvas, bg="#f0f8ff") # outline of each pet

# Configure scrolling
pet_list_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=pet_list_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

# Pack scrollable components
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Bind search entry to refresh on Enter key
search_entry.bind('<Return>', lambda event: refresh_pet_list())

# Bind category selection to refresh
category_var.trace('w', lambda *args: refresh_pet_list())

# Initial load of pets
refresh_pet_list()

if __name__ == "main":root.mainloop()