import streamlit as st
import json
import os

# ---------- File Handling ----------
LIBRARY_FILE = 'library.json'

def load_library():
    if os.path.exists(LIBRARY_FILE):
        with open(LIBRARY_FILE, 'r') as f:
            return json.load(f)
    return []

def save_library(library):
    with open(LIBRARY_FILE, 'w') as f:
        json.dump(library, f, indent=4)

# ---------- Core Functions ----------
def add_book(library, book):
    library.append(book)
    save_library(library)

def remove_book(library, title):
    updated_library = [book for book in library if book['title'].lower() != title.lower()]
    save_library(updated_library)
    return updated_library

def search_books(library, query):
    query = query.lower()
    return [book for book in library if query in book['title'].lower() or query in book['author'].lower()]

def display_statistics(library):
    total = len(library)
    read = sum(1 for book in library if book['read'])
    percentage = (read / total * 100) if total else 0
    return total, percentage

def display_book(book):
    st.write(f"📖 **Title**: {book['title']}")
    st.write(f"✍️ **Author**: {book['author']}")
    st.write(f"📅 **Year**: {book['year']}")
    st.write(f"🎭 **Genre**: {book['genre']}")
    st.write(f"✅ **Read**: {'Yes' if book['read'] else 'No'}")
    st.markdown("---")

# ---------- Streamlit UI ----------
st.title("📚 Personal Library Manager")

library = load_library()

menu = st.sidebar.selectbox("Menu", ["Add a Book", "Remove a Book", "Search for a Book", "Display All Books", "Display Statistics"])

if menu == "Add a Book":
    st.header("➕ Add a New Book")
    title = st.text_input("Title")
    author = st.text_input("Author")
    year = st.number_input("Publication Year", min_value=0, max_value=9999, step=1)
    genre = st.text_input("Genre")
    read = st.checkbox("Have you read it?")
    
    if st.button("Add Book"):
        if title and author and genre:
            book = {
                'title': title,
                'author': author,
                'year': int(year),
                'genre': genre,
                'read': read
            }
            add_book(library, book)
            st.success(f"Book '{title}' added to your library!")
        else:
            st.warning("Please fill out all fields.")

elif menu == "Remove a Book":
    st.header("❌ Remove a Book")
    title_to_remove = st.text_input("Enter the title of the book to remove")
    if st.button("Remove"):
        library = remove_book(library, title_to_remove)
        st.success(f"Book '{title_to_remove}' removed (if it existed).")

elif menu == "Search for a Book":
    st.header("🔍 Search Books")
    query = st.text_input("Search by title or author")
    if query:
        results = search_books(library, query)
        if results:
            st.write(f"Found {len(results)} result(s):")
            for book in results:
                display_book(book)
        else:
            st.info("No matching books found.")

elif menu == "Display All Books":
    st.header("📚 Your Book Collection")
    if library:
        for book in library:
            display_book(book)
    else:
        st.info("Your library is empty.")

elif menu == "Display Statistics":
    st.header("📊 Library Statistics")
    total, percentage = display_statistics(library)
    st.write(f"**Total Books**: {total}")
    st.write(f"**Read Percentage**: {percentage:.2f}%")

