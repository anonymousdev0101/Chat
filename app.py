import streamlit as st
import requests
from datetime import datetime
import base64

# GitHub credentials and repository details
GITHUB_TOKEN = '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'  # Your GitHub token
REPO_OWNER = 'anonymousdev0101'  # Your GitHub username
REPO_NAME = 'Chat'  # Your GitHub repository name
FILE_PATH = 'data.txt'  # Path to the file in your repo

# GitHub API URL to access the file in the repository
url = f'https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{FILE_PATH}'

# Function to fetch the current chat history from the GitHub file
def fetch_chat_history():
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        file_content = response.json()['content']
        # Decode the content from Base64
        decoded_content = base64.b64decode(file_content).decode('utf-8')
        return decoded_content.split('\n')
    else:
        st.error(f"Error fetching chat history from GitHub: {response.status_code}")
        return []

# Function to save a new chat message to the GitHub file
def save_message(message):
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_message = f"{current_time} - {message}"

    # Fetch current content and append the new message
    chat_history = fetch_chat_history()
    chat_history.append(new_message)
    
    # Prepare the updated content (join all messages)
    updated_content = "\n".join(chat_history)
    
    # Convert the content to Base64 for GitHub API
    encoded_content = base64.b64encode(updated_content.encode('utf-8')).decode('utf-8')
    
    # Fetch the file details to get the 'sha' value
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        sha = response.json()['sha']
    else:
        st.error(f"Error fetching file details: {response.status_code}")
        return
    
    # Update the file on GitHub with the new content
    update_response = requests.put(
        url,
        headers=headers,
        json={
            "message": "Update chat history",
            "content": encoded_content,
            "sha": sha
        }
    )

    if update_response.status_code == 200:
        st.success("Message saved successfully!")
    else:
        st.error(f"Error saving message: {update_response.status_code}")

# Streamlit App
def main():
    st.title("Anonymous Chat")

    # Display chat history
    st.subheader("Chat History")
    messages = fetch_chat_history()
    for message in messages:
        st.write(message)

    # Input box for the new message
    new_message = st.text_input("Your message:")
    if st.button("Send"):
        if new_message:
            save_message(new_message)
            st.experimental_rerun()  # Refresh the page to show the new message
        else:
            st.warning("Please enter a message before sending.")

if __name__ == "__main__":
    main()
