import tkinter as tk
from tkinter import messagebox
import random
import csv
import xml.etree.ElementTree as ET
from datetime import datetime

# Function to read names from a file
def read_names_from_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        names = file.read().splitlines()
    return names

# Read names from files
female_first_names = read_names_from_file('ressources/female_first_names.txt')
male_first_names = read_names_from_file('ressources/male_first_names.txt')
last_names = read_names_from_file('ressources/family_names.txt')

# Function to generate random date of birth
def generate_random_date(start_year=2002, end_year=2005):
    start_date = datetime(year=start_year, month=1, day=1)
    end_date = datetime(year=end_year, month=12, day=31)
    random_date = start_date + (end_date - start_date) * random.random()
    return random_date.strftime("%d/%m/%Y")

# Function to generate random student data
def generate_student_data(num_students, class_name, start_year, end_year):
    student_data = []
    for _ in range(num_students):
        if random.random() < 0.5:
            first_name = random.choice(female_first_names)
            sex = "F"
        else:
            first_name = random.choice(male_first_names)
            sex = "M"
        last_name = random.choice(last_names)
        dob = generate_random_date(start_year, end_year)
        student_data.append([last_name, first_name, sex, dob, class_name])
    return student_data

# Function to save data to a file
def save_data(student_data, file_format):
    if file_format == "CSV":
        with open('students.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Nom", "Prénom", "Sexe", "Date de naissance", "Classe"])
            writer.writerows(student_data)
    elif file_format == "TXT":
        with open('students.txt', mode='w', encoding='utf-8') as file:
            for student in student_data:
                file.write(" | ".join(student) + "\n")
    elif file_format == "XML":
        root = ET.Element("Students")
        for student in student_data:
            student_elem = ET.SubElement(root, "Student")
            ET.SubElement(student_elem, "LastName").text = student[0]
            ET.SubElement(student_elem, "FirstName").text = student[1]
            ET.SubElement(student_elem, "Sex").text = student[2]
            ET.SubElement(student_elem, "DOB").text = student[3]
            ET.SubElement(student_elem, "Class").text = student[4]
        tree = ET.ElementTree(root)
        tree.write("students.xml", encoding='utf-8')
    messagebox.showinfo("Succès", f"Les données ont été enregistrées dans 'students.{file_format.lower()}'.")

# Function to generate and save student data based on user input
def generate_and_save():
    class_name = class_entry.get()
    try:
        num_students = int(num_students_entry.get())
        start_year = int(start_year_entry.get())
        end_year = int(end_year_entry.get())
        file_format = format_var.get()
        student_data = generate_student_data(num_students, class_name, start_year, end_year)
        save_data(student_data, file_format)
    except ValueError:
        messagebox.showerror("Erreur", "Veuillez entrer des valeurs valides.")

# Tkinter GUI setup
root = tk.Tk()
root.title("Générateur d'élèves")

# Labels and entries
tk.Label(root, text="Classe:").grid(row=0, column=0)
class_entry = tk.Entry(root)
class_entry.grid(row=0, column=1)

tk.Label(root, text="Nombre d'élèves:").grid(row=1, column=0)
num_students_entry = tk.Entry(root)
num_students_entry.grid(row=1, column=1)

tk.Label(root, text="Année de naissance (début):").grid(row=2, column=0)
start_year_entry = tk.Entry(root)
start_year_entry.grid(row=2, column=1)

tk.Label(root, text="Année de naissance (fin):").grid(row=3, column=0)
end_year_entry = tk.Entry(root)
end_year_entry.grid(row=3, column=1)

# File format options
tk.Label(root, text="Format de fichier:").grid(row=4, column=0)
format_var = tk.StringVar(value="CSV")
formats = ["CSV", "TXT", "XML"]
for idx, format in enumerate(formats):
    tk.Radiobutton(root, text=format, variable=format_var, value=format).grid(row=4, column=idx+1)

# Generate button
generate_button = tk.Button(root, text="Générer fichier", command=generate_and_save)
generate_button.grid(row=5, columnspan=3, pady=10)

root.mainloop()
