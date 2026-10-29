"use strict";

// Dismiss feedback messages without needing a page refresh.
document.addEventListener("click", (event) => {
    const closeButton = event.target.closest(".message-close");
    if (closeButton) {
        const message = closeButton.closest(".message");
        if (message) message.remove();
    }
});

// Ask the user before sending a form that declares a confirmation message.
document.addEventListener("submit", (event) => {
    const form = event.target;
    const confirmation = form.getAttribute("data-confirm");
    if (confirmation && !window.confirm(confirmation)) {
        event.preventDefault();
    }
});
