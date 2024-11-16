import streamlit as st
import sqlite3
from datetime import datetime

# Set up SQLite database connection
conn = sqlite3.connect('chat_db.db')
cursor = conn.cursor()

# Create a table for storing chat messages (if it doesn't exist)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        message TEXT,
        timestamp TEXT
    )
''')
conn.commit()

# Function to fetch all chat messages
def get_messages():
    cursor.execute("SELECT message, timestamp FROM messages ORDER BY timestamp ASC")
    return cursor.fetchall()

# Function to save a new chat message
def save_message(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO messages (message, timestamp) VALUES (?, ?)", (message, timestamp))
    conn.commit()

# Streamlit app
def main():
    st.title("Anonymous Chat")

    # Display existing messages
    st.subheader("Chat History")
    messages = get_messages()
    for msg, timestamp in messages:
        st.write(f"{timestamp} - {msg}")

    # Input box for the new message
    new_message = st.text_input("Your message:")
    if st.button("Send"):
        if new_message:
            save_message(new_message)
            st.experimental_rerun()  # Refresh the page to show new message
        else:
            st.warning("Please enter a message before sending.")

if __name__ == "__main__":
    main()
