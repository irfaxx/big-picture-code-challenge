#!/usr/bin/env python
# coding: utf-8

# In[46]:


import requests
import json
import mysql.connector
from mysql.connector import Error

# Get input from the user 
isbn = input("Enter ISBN number: ")

# Print the user's input
print("You entered:", isbn)

# Defining the URLs using the GET URL
get_url = f"https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&jscmd=data&format=json"

# Initialize a dictionary to store the data
book_info = {"title": "", "authors": [], "summary": "", "cover_url": ""}

# Make a GET request to retrieve data
response = requests.get(get_url)

# Checking if the GET request was successful 
if response.status_code == 200:
    try:
        # converting the response data into Json
        response_content = response.json()

        # Check if the ISBN exists in the JSON response
        isbn_key = f"ISBN:{isbn}"
        if isbn_key in response_content:
            isbn_data = response_content[isbn_key]
            
            #Extract the fields that are required to store
            # Extract title
            title = isbn_data.get("title", "Title not found")
            book_info["title"] = title

            # Extract authors as a list of names
            authors_list = isbn_data.get("authors", [{"name": "Author not found"}])
            author_names = [author["name"] for author in authors_list]
            book_info["authors"] = author_names

            # Extract summary if available
            if "description" in isbn_data:
                summary = isbn_data["description"]["value"]
                book_info["summary"] = summary

            # Extract cover URL
            cover_url = isbn_data.get("cover", {}).get("large", "Cover URL not found")
            book_info["cover_url"] = cover_url

        else:
            print(f"ISBN {isbn} not found in the JSON response.")
    except ValueError as e:
        print("Error: Unable to parse JSON response.")
else:
    print("GET request failed with status code:", response.status_code)



# Print the JSON data (as in your new code)
print("JSON Data:")
print(book_info_json)

# MySQL database configuration
db_config = {
    "host": "localhost",
    "user": "Irfan",
    "password": "*********",
    "database": "BigPicture",
}

# JSON data to insert
book_info_json = json.dumps(book_info, indent=4)

# Create a connection to the MySQL database
try:
    connection = mysql.connector.connect(**db_config)

    if connection.is_connected():
        cursor = connection.cursor()
        
        #Insertion of the book queries into the table 
        insert_query = "INSERT INTO books (json_data) VALUES (%s)"

       
        data_to_insert = (book_info_json,)

        # query execution
        cursor.execute(insert_query, data_to_insert)

        # transaction
        connection.commit()

        print("JSON data inserted successfully!")
        

        # Selection of the data from the table
        select_query = "SELECT json_data FROM books"

        cursor.execute(select_query)

        rows = cursor.fetchall()

        # Displaying
        for row in rows:
            book_info_json = row[0]
            print("JSON Data:")
            print(book_info_json)

except Error as e:
    print(f"Error: {e}")

finally:
    # Close the cursor and connection
    if connection.is_connected():
        cursor.close()
        connection.close()






