
// to scroll bottom of the chat box on the loading
const chatMainContainer = document.getElementById('chatMainContainer'),
    chatUniqueCode = document.getElementById('chatUniqueCode').innerHTML;
window.addEventListener('load', () => {
    chatMainContainer.scrollTo(0, chatMainContainer.scrollHeight)
})







websocket = new WebSocket(
    'ws://' + window.location.host + '/ws/chat/' + chatUniqueCode + '/'
);




const myUsername = document.getElementById('myUsername').innerHTML;
websocket.addEventListener('message', (e) => {
    let data = JSON.parse(e.data);
    if (data['message'] === 'group_deleted') {
        if (data['sender'] !== myUsername) {
            alert('Chat is deleted by its owner.');
            window.location.href = window.location.origin;
        }
    }
    else if (data['message'] === 'member_left' && data['activity_msg']) {
        let x = document.createElement('div');
        x.classList.add('activityChat');
        x.innerHTML = `<div class="chatText activityMsg">${data["sender"]} has left this group</div>`;
        chatMainContainer.appendChild(x);
        chatMainContainer.scrollTo(0, chatMainContainer.scrollHeight);
    }
    else if (data['message'] === 'member_joined' && data['activity_msg']) {
        let x = document.createElement('div');
        x.classList.add('activityChat');
        x.innerHTML = `<div class="chatText activityMsg">${data["sender"]} has joined in this group</div>`;
        chatMainContainer.appendChild(x);
        chatMainContainer.scrollTo(0, chatMainContainer.scrollHeight);
    }
    else {
        if (data['sender'] === myUsername) {
            let x = document.createElement('div');
            x.classList.add('myChat');
            x.innerHTML = `<strong>You (${new Date().toLocaleTimeString("UTC", {hour: '2-digit', minute: '2-digit'})})</strong>  <div class="chatText">${data["message"]}</div>`;
            chatMainContainer.appendChild(x);
            chatMainContainer.scrollTo(0, chatMainContainer.scrollHeight);
        } else {
            let x = document.createElement('div');
            x.classList.add('theirChat');
            x.innerHTML = `<strong>${data['sender']} (${new Date().toLocaleTimeString("UTC", {hour: '2-digit', minute: '2-digit'})})</strong>  <div class="chatText">${data["message"]}</div>`;
            chatMainContainer.appendChild(x)
            chatMainContainer.scrollTo(0, chatMainContainer.scrollHeight);
        }
    }

});



let messageSendBtn = document.getElementById('messageSendBtn'),
    messageText = document.getElementById('messageText');
messageSendBtn.addEventListener('click', () => {
    let message = messageText.value;
    if (message !== '') {
        websocket.send(JSON.stringify({'message': message}));
        messageText.value = '';
    }
});