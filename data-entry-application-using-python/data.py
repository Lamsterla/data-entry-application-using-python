from tkinter import *
import sqlite3

root = Tk()
root.title("File Dialogue Box")
root.iconbitmap(r"C:\Users\rahul  sah\Desktop\pycharm")  # Ensure the path is correct
root.geometry("400x400")

# Connect to SQLite DB and create a cursor
conn = sqlite3.connect("address_book.db")
c = conn.cursor()

# Create table (only once, the table will persist after the first creation)
c.execute("""CREATE TABLE IF NOT EXISTS addresses (
                first_name text,
                last_name text,
                address text,
                city text,
                state text,
                zipcode integer)""")
conn.commit()  # Commit the table creation if it's a new one

# Function to update a record in the database
def update(record_id):
    conn = sqlite3.connect("address_book.db")
    c = conn.cursor()

    c.execute("""UPDATE addresses SET
    first_name =:first,
    last_name =:last,
    address =:address,
    city =:city,
    state =:state,
    zipcode=:zipcode
    WHERE oid=:oid""",
    {'first': f_name_editor.get(),
     'last': l_name_editor.get(),
     'address': address_editor.get(),
     'city': city_editor.get(),
     'state': state_editor.get(),
     'zipcode': zipcode_editor.get(),
     'oid': record_id})

    conn.commit()
    conn.close()

    editor.destroy()

# Function to edit a record
def edit():
    global editor
    record_id = select_id_entry.get()  # Fetch ID to edit from the Entry field
    if not record_id:
        print("Please provide a valid ID to edit.")
        return

    editor = Tk()
    editor.title("Update Record")
    editor.iconbitmap(r"C:\Users\rahul  sah\Desktop\pycharm")  # Ensure the path is correct
    editor.geometry("400x400")

    conn = sqlite3.connect("address_book.db")
    c = conn.cursor()

    # Fetch the record from the database using the provided ID
    c.execute("SELECT * FROM addresses WHERE oid = ?", (record_id,))
    record = c.fetchone()

    if record:
        global f_name_editor, l_name_editor, address_editor, city_editor, state_editor, zipcode_editor

        # Entry fields for editing
        f_name_editor = Entry(editor, width=30)
        f_name_editor.grid(row=0, column=1, padx=20)
        l_name_editor = Entry(editor, width=30)
        l_name_editor.grid(row=1, column=1)
        address_editor = Entry(editor, width=30)
        address_editor.grid(row=2, column=1)
        city_editor = Entry(editor, width=30)
        city_editor.grid(row=3, column=1)
        state_editor = Entry(editor, width=30)
        state_editor.grid(row=4, column=1)
        zipcode_editor = Entry(editor, width=30)
        zipcode_editor.grid(row=5, column=1)

        # Labels
        f_name_label_edit = Label(editor, text="First Name")
        f_name_label_edit.grid(row=0, column=0)
        l_name_label_edit = Label(editor, text="Last Name")
        l_name_label_edit.grid(row=1, column=0)
        address_label_edit = Label(editor, text="Address")
        address_label_edit.grid(row=2, column=0)
        city_label_edit = Label(editor, text="City")
        city_label_edit.grid(row=3, column=0)
        state_label_edit = Label(editor, text="State")
        state_label_edit.grid(row=4, column=0)
        zipcode_label_edit = Label(editor, text="Zipcode")
        zipcode_label_edit.grid(row=5, column=0)

        # Populate the entry fields with the existing data
        f_name_editor.insert(0, record[0])
        l_name_editor.insert(0, record[1])
        address_editor.insert(0, record[2])
        city_editor.insert(0, record[3])
        state_editor.insert(0, record[4])
        zipcode_editor.insert(0, record[5])

        # Save button to update the record
        save_button = Button(editor, text="Save Changes", command=lambda: update(record_id))
        save_button.grid(row=6, column=0, pady=10, columnspan=2, padx=30, ipadx=100)

    else:
        print("Record not found.")
    conn.close()

# Function to delete a record
def delete():
    record_id = select_id_entry.get()  # Get the ID to delete
    if not record_id:
        print("Please provide a valid ID to delete.")
        return

    conn = sqlite3.connect("address_book.db")
    c = conn.cursor()

    # Delete the record from the database
    c.execute("DELETE FROM addresses WHERE oid = ?", (record_id,))
    conn.commit()  # Commit the changes
    conn.close()

    select_id_entry.delete(0, END)  # Clear the Entry field for ID

# Function to submit a new record
def submit():
    conn = sqlite3.connect("address_book.db")
    c = conn.cursor()

    # Insert into the table
    c.execute("INSERT INTO addresses (first_name, last_name, address, city, state, zipcode) VALUES (?, ?, ?, ?, ?, ?)",
              (f_name.get(), l_name.get(), address.get(), city.get(), state.get(), zipcode.get()))

    conn.commit()  # Commit the changes
    conn.close()

    # Clear the entry fields after submission
    f_name.delete(0, END)
    l_name.delete(0, END)
    address.delete(0, END)
    city.delete(0, END)
    state.delete(0, END)
    zipcode.delete(0, END)

# Function to query and display all records
def query():
    conn = sqlite3.connect("address_book.db")
    c = conn.cursor()

    c.execute("SELECT *, oid FROM addresses")
    records = c.fetchall()

    for widget in query_frame.winfo_children():
        widget.destroy()

    row = 1
    for record in records:
        record_str = f"{record[0]} {record[1]}, {record[2]}, {record[3]}, {record[4]}, {record[5]}, {record[6]}"
        record_label = Label(query_frame, text=record_str)
        record_label.grid(row=row, column=0)
        row += 1

    conn.close()

# Entry fields for user input
f_name = Entry(root, width=30)
f_name.grid(row=0, column=1, padx=20)

l_name = Entry(root, width=30)
l_name.grid(row=1, column=1)

address = Entry(root, width=30)
address.grid(row=2, column=1)

city = Entry(root, width=30)
city.grid(row=3, column=1)

state = Entry(root, width=30)
state.grid(row=4, column=1)

zipcode = Entry(root, width=30)
zipcode.grid(row=5, column=1)

first_label=Label(root,text="first name")
first_label.grid(row=0,column=0)
last_name_label=Label(root,text="last name")
last_name_label.grid(row=1,column=0)
address_label=Label(root,text="address")
address_label.grid(row=2,column=0)
city_label=Label(root,text="city")
city_label.grid(row=3,column=0)
state_label=Label(root,text="state")
state_label.grid(row=4,column=0)
zipcode_label=Label(root,text="zipcode")
zipcode_label.grid(row=5,column=0)

select_id_entry = Entry(root, width=30)  # Entry field for ID to edit or delete
select_id_entry.grid(row=9, column=1)

# Create buttons
delete_button = Button(root, text="Delete Record", command=delete)
delete_button.grid(row=10, column=0, pady=10, columnspan=2, padx=30, ipadx=100)

edit_button = Button(root, text="Edit Record", command=edit)
edit_button.grid(row=11, column=0, pady=10, columnspan=2, padx=30, ipadx=100)

submit_button = Button(root, text="Submit", command=submit)
submit_button.grid(row=6, column=0, pady=10, columnspan=2, padx=30, ipadx=100)

query_button = Button(root, text="Query", command=query)
query_button.grid(row=7, column=0, pady=10, columnspan=2, padx=30, ipadx=100)

# Create labels
select_id_label = Label(root, text="Select ID to edit or delete")
select_id_label.grid(row=9, column=0)

# Frame to display query results
query_frame = Frame(root)
query_frame.grid(row=8, column=0, columnspan=2, pady=10)

root.mainloop()
