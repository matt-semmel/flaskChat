document.addEventListener('DOMContentLoaded', function () {
  // Retrieve the current username from the hidden input field
  const currentUsername = document.getElementById('current-username').value;

  // Fetch all chat messages and update the chat box
  function fetchMessages() {
    fetch('/messages/')
      .then((response) => response.json())
      .then((data) => {
        const chatBox = document.getElementById('chat-box');
        chatBox.innerHTML = '';

        data.forEach((message) => {
          const chatMessage = document.createElement('div');
          if (message.author === currentUsername) {
            chatMessage.className = 'own-message'; // Style user's own messages differently
          } else {
            chatMessage.className = 'other-message'; // Style messages from other users differently
          }
          chatMessage.innerHTML = `<strong>${message.author}: </strong>${message.message}`;
          chatBox.appendChild(chatMessage);
        });
      })
      .catch((error) => {
        console.error('Error fetching messages:', error);
      });
  }

  // Function to send a new chat message to the server
  function sendMessage() {
    const messageInput = document.getElementById('message');
    const message = messageInput.value.trim();
    if (message !== '') {
      const username = document.getElementById('current-username').value;
      fetch('/new_message/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        },
        body: `username=${username}&message=${message}`,
      })
        .then(() => {
          messageInput.value = '';
          fetchMessages(); // Fetch and update messages immediately after sending a new message
        })
        .catch((error) => {
          console.error('Error sending message:', error);
        });
    }
  }

  // Event listener for the chat form submission
  const chatForm = document.getElementById('chat-form');
  chatForm.addEventListener('submit', function (event) {
    event.preventDefault();
    sendMessage();
  });

  // Initial fetch of messages when the page loads
  fetchMessages();

  // Fetch and update messages every 15 seconds
  setInterval(fetchMessages, 15000);
});

// Logout user and return to login screen
function logout() {
    fetch('/logout/')
      .then(() => {
        window.location.href = '/login/';
      })
      .catch((error) => {
        console.error('Error during logout:', error);
      });
  }

  // Event listener for the logout button
  const logoutButton = document.getElementById('logout-btn');
  logoutButton.addEventListener('click', function () {
    logout();
  });