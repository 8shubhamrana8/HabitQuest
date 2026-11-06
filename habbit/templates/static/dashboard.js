

document.querySelectorAll('.habit-toggle').forEach(checkbox => {
    checkbox.addEventListener('change', function() {
        const habitId = this.dataset.habitId; // Get current habitId
        
        const currentCheckbox = this; 

        fetch('/update_log/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: JSON.stringify({
                habit_id: habitId 
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                // Change streak and update user total_xp
                document.querySelector(`#streak-${habitId}`).innerText = data.current_streak;
                document.querySelector('#user-total-xp').innerText = data.total_xp;
                
                // Update last logged in badge
                const dateBadge = document.querySelector(`#last-logged-${habitId}`);
                if (dateBadge) {
                    dateBadge.innerText = `Last Logged: ${data.last_logged_date}`;
                }
                
                // // Disable the checkbox so that user cannot input any more
                currentCheckbox.disabled = true;
                
                // Update XP text
                const xpElement = document.getElementById("user-total-xp");
                    if (xpElement && data.total_xp !== undefined) {
                        xpElement.textContent = data.total_xp;
                    }

                // Update Rank Badge Image
                const userBadge = document.getElementById("user-badge");
                if (userBadge && data.new_rank_badge) {
                    userBadge.src = data.new_rank_badge;
                }

                //Update Rank Title Text
                const userRank = document.getElementById("user-rank");
                if (userRank && data.new_rank_title) {
                    userRank.textContent = data.new_rank_title;
                }
                
            } else if (data.status === 'ignored') {
                currentCheckbox.checked = true;
                currentCheckbox.disabled = true;
            }
        })
        .catch(error => console.error('Error:', error));
    });
});


// Delete habit

document.querySelectorAll('.delete-habit-btn').forEach(button => {
    button.addEventListener('click', function(event) {
        const habitId = this.dataset.habitId; // Get current habitId

        const currentBtn = this; 

        fetch('/delete_habit/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: JSON.stringify({
                habit_id: habitId 
            })
        }).then(response => response.json())
        .then(data => {
            if (data.status === "success") {
                const habitCard = document.getElementById(`habit-card-${habitId}`);
                if (habitCard) {
                    habitCard.remove();
                }
            }
        })
        .catch(error => console.error('Error:', error));
    })
})