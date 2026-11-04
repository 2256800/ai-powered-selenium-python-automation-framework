function togglePassword(inputId, button) {
    const passwordInput = document.getElementById(inputId);

    if (passwordInput.type === "password") {
        passwordInput.type = "text";

        button.innerHTML = `
            <svg width="22" height="22" viewBox="0 0 24 24"
                 fill="none" stroke="currentColor"
                 stroke-width="2" stroke-linecap="round"
                 stroke-linejoin="round">
                <path d="M3 3l18 18"></path>
                <path d="M10.6 10.6a2 2 0 002.8 2.8"></path>
                <path d="M9.9 5.2A10.8 10.8 0 0112 5
                         c5 0 9 7 9 7a15 15 0 01-3 3.5"></path>
                <path d="M6.2 6.2C4.2 7.5 3 12 3 12
                         s4 7 9 7c1.2 0 2.3-.3 3.3-.8"></path>
            </svg>`;
    } else {
        passwordInput.type = "password";

        button.innerHTML = `
            <svg width="22" height="22" viewBox="0 0 24 24"
                 fill="none" stroke="currentColor"
                 stroke-width="2" stroke-linecap="round"
                 stroke-linejoin="round">
                <path d="M2 12s3.5-7 10-7 10 7 10 7
                         -3.5 7-10 7S2 12 2 12z"></path>
                <circle cx="12" cy="12" r="3"></circle>
            </svg>`;
    }
}