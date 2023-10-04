/* Javascript for ChatGPTXBlock. */
function ChatGPTXBlock(runtime, element) {
    // UI Elements
    let chatMsg = document.getElementById('chat-msg');
    let chatLogs = document.getElementById('chat-logs');
    let sendBtn = document.getElementById('send-btn');
    let errorMsg = document.getElementById('error-msg');
    let loadingMsg = document.createElement('div');
    loadingMsg.textContent = "";
    loadingMsg.classList.add("loading");
    // Handlers
    var handlerUrl = runtime.handlerUrl(element, 'send_message');

    function send_message(message) {
        return $.ajax({
            type: "POST",
            url: handlerUrl,
            data: JSON.stringify({"message": message}),
            contentType:"application/json; charset=utf-8",
            dataType: "json",
        }).done(function(response) {
            if (response.result === 'success') {
                chatLogs.removeChild(loadingMsg);
                type_message(response.response);
            } else {
                alert('Oops, something went wrong!');
            }
        }).fail(function(error) {
            console.log("An error occurred: ", error);
        });
    };

    sendBtn.addEventListener('click', function() {
        if (!chatMsg.value.trim()) {
            errorMsg.textContent = "You should ask a question";
            return;
        }
        errorMsg.textContent = "";
        let newMsg = document.createElement('div');
        newMsg.textContent = chatMsg.value;
        newMsg.classList.add("my-msg");
        chatLogs.appendChild(newMsg);
        chatLogs.appendChild(loadingMsg);

        chatMsg.value = "";
        // Call the Python function with the message as input
        send_message(newMsg.textContent);
    });
    function type_message(message) {
        let i = 0;
        let aiMsg = document.createElement('div');
        aiMsg.classList.add("ai-msg");
        chatLogs.appendChild(aiMsg);
        let typing = setInterval(function() {
            if (i < message.length) {
                aiMsg.textContent += message.charAt(i);
                i++;
            } else {
                clearInterval(typing);
            }
        }, 10);  // The number 100 here represents the speed of the typing (in this case, 100 ms delay between each letter)
    }
    $(function ($) {
        /* Here's where you'd do things on page load. */
    });
}
