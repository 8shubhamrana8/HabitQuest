document.addEventListener('DOMContentLoaded', () => {
    // 1. Extract the CSRF Token for security
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    
    // 2. Select the comment submission button
    const postBtn = document.getElementById('post-comment-btn');
    if (postBtn) {
        postBtn.addEventListener('click', function() {
            const inputField = document.getElementById('comment-input');
            const commentText = inputField.value.trim();
            const profileId = this.dataset.profileId; // Reads data-profile-id from the HTML
            
            if (commentText === "") return; // Don't post empty comments
            
            // 3. Send the POST request securely
            fetch('/add_comment/' + profileId + '/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken // Pass securely within your fetch headers
                },
                body: JSON.stringify({
                    profile_id: profileId,
                    comment: commentText
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    // 4. Clear the input field
                    inputField.value = '';
                    
                    // 5. Remove the "No comments yet" message if it exists
                    const noCommentsMsg = document.getElementById('no-comments-msg');
                    if (noCommentsMsg) noCommentsMsg.remove();
                    
                    // 6. Build the new HTML element dynamically
                    const commentsContainer = document.getElementById('comments-container');
                    const newCommentHtml = `
                        <div class="mb-3 border-bottom pb-2">
                            <p class="mb-1 fw-bold text-primary">
                                @${data.username} 
                                <span class="text-muted small fw-normal">(${data.formatted_time})</span>
                            </p>
                            <p class="mb-0 text-light">${data.comment}</p>
                        </div>
                    `;
                    
                    // 7. Insert the new comment at the very top of the list
                    commentsContainer.insertAdjacentHTML('afterbegin', newCommentHtml);
                }
            })
            .catch(error => console.error('Error posting comment:', error));
        });
    }
});