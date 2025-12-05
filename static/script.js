document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chat-form');
    const messageInput = document.getElementById('message-input');
    const chatWindow = document.getElementById('chat-window');
    const welcomeContainer = document.getElementById('welcome-container');
    const sendButton = document.getElementById('send-button');
    const examplePromptsContainer = document.querySelector('.example-prompts');
    const themeToggle = document.getElementById('theme-toggle');
    const sunIcon = document.getElementById('sun-icon');
    const moonIcon = document.getElementById('moon-icon');

    // Theme Toggle Logic
    function setTheme(isDark) {
        if (isDark) {
            document.body.classList.add('dark-mode');
            sunIcon.style.display = 'block';
            moonIcon.style.display = 'none';
            localStorage.setItem('theme', 'dark');
        } else {
            document.body.classList.remove('dark-mode');
            sunIcon.style.display = 'none';
            moonIcon.style.display = 'block';
            localStorage.setItem('theme', 'light');
        }
    }

    // Check for saved theme preference or system preference
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        setTheme(true);
    } else if (savedTheme === 'light') {
        setTheme(false);
    } else {
        // Default to light mode if no preference, or check system preference
        // const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        // setTheme(systemPrefersDark);
        setTheme(false); // Default to light as per CSS default
    }

    if (themeToggle) {
        themeToggle.addEventListener('click', () => {
            const isDark = document.body.classList.contains('dark-mode');
            setTheme(!isDark);
        });
    }
    const historyList = document.getElementById('history-list');
    let currentChatId = null;

    // Load history on startup
    loadHistory();

    async function loadHistory() {
        try {
            const response = await fetch('/history');
            const data = await response.json();
            currentChatId = data.currentChatId;
            renderHistory(data.history);
        } catch (error) {
            console.error('Error loading history:', error);
        }
    }

    function renderHistory(history) {
        if (!historyList) return;
        historyList.innerHTML = '';

        history.forEach(chat => {
            const item = document.createElement('div');
            item.classList.add('history-item');
            if (chat.id === currentChatId) {
                item.classList.add('active');
            }
            item.textContent = chat.title || 'Nouvelle conversation';
            item.addEventListener('click', () => loadChat(chat.id));
            historyList.appendChild(item);
        });
    }

    async function loadChat(chatId) {
        if (chatId === currentChatId) return;

        try {
            const response = await fetch(`/load_chat/${chatId}`);
            const data = await response.json();

            if (data.error) {
                console.error(data.error);
                return;
            }

            // Clear current chat
            chatWindow.innerHTML = '';
            hideWelcomeScreen();

            // Render messages
            data.messages.forEach(msg => {
                addMessageToWindow(msg.content, msg.sender);
            });

            currentChatId = chatId;

            // Update active state in history list
            document.querySelectorAll('.history-item').forEach(item => {
                item.classList.remove('active');
            });
            // We might need to re-render history to set active class correctly if we don't have reference to the element
            loadHistory();

        } catch (error) {
            console.error('Error loading chat:', error);
        }
    }

    // New Chat Logic
    const newChatBtn = document.querySelector('.new-chat-btn');
    if (newChatBtn) {
        newChatBtn.addEventListener('click', async () => {
            // Clear chat window
            chatWindow.innerHTML = '';

            // Show welcome screen
            if (welcomeContainer) {
                welcomeContainer.classList.remove('hidden');
            }

            // Reset backend session
            try {
                await fetch('/reset', { method: 'POST' });
                loadHistory(); // Refresh history to show new chat (or clear selection)
            } catch (error) {
                console.error('Error resetting chat:', error);
            }
        });
    }

    // Function to hide the welcome screen
    function hideWelcomeScreen() {
        if (welcomeContainer && !welcomeContainer.classList.contains('hidden')) {
            welcomeContainer.classList.add('hidden');
        }
    }

    // Adjust textarea height automatically
    function adjustTextareaHeight() {
        messageInput.style.height = 'auto';
        messageInput.style.height = messageInput.scrollHeight + 'px';
    }
    messageInput.addEventListener('input', adjustTextareaHeight);

    // Handle Enter to send, Shift+Enter for new line
    messageInput.addEventListener('keydown', (event) => {
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault();
            sendButton.click();
        }
    });

    // Handle clicking on example prompts
    if (examplePromptsContainer) {
        examplePromptsContainer.addEventListener('click', (event) => {
            if (event.target.classList.contains('prompt')) {
                const promptText = event.target.textContent.replace(/"/g, ''); // Remove quotes
                messageInput.value = promptText;
                adjustTextareaHeight();
                sendButton.click();
            }
        });
    }

    chatForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        const message = messageInput.value.trim();

        if (message) {
            hideWelcomeScreen();
            addMessageToWindow(message, 'user');
            messageInput.value = '';
            adjustTextareaHeight();
            showThinkingIndicator();

            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ message: message }),
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                const data = await response.json();
                hideThinkingIndicator();
                addMessageToWindow(data.response, 'bot');

                // Refresh history to update titles or add new chat
                loadHistory();

            } catch (error) {
                console.error('Error fetching chat response:', error);
                hideThinkingIndicator();
                addMessageToWindow('Oops! Quelque chose a mal tourné.', 'bot');
            }
        }
    });

    function addMessageToWindow(content, sender, isThinking = false) {
        const messageWrapper = document.createElement('div');
        messageWrapper.classList.add('message-wrapper', `${sender}-wrapper`);

        const contentContainer = document.createElement('div');
        contentContainer.classList.add('message-content-container');

        const avatar = document.createElement('div');
        avatar.classList.add('avatar');
        avatar.textContent = sender === 'user' ? 'U' : 'CB';

        const messageElement = document.createElement('div');
        messageElement.classList.add('message', `${sender}-message`);

        if (isThinking) {
            messageWrapper.id = 'thinking-indicator';
            messageElement.innerHTML = '<span class="dot"></span><span class="dot"></span><span class="dot"></span>';
        } else {
            const p = document.createElement('p');
            // Replace newline characters with <br> for proper HTML rendering
            p.innerHTML = content.replace(/\n/g, '<br>');
            messageElement.appendChild(p);
        }

        contentContainer.appendChild(avatar);
        contentContainer.appendChild(messageElement);
        messageWrapper.appendChild(contentContainer);

        chatWindow.appendChild(messageWrapper);
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }

    function showThinkingIndicator() {
        addMessageToWindow('', 'bot', true); // Pass empty content
    }

    function hideThinkingIndicator() {
        const indicator = document.getElementById('thinking-indicator');
        if (indicator) {
            indicator.remove();
        }
    }
});