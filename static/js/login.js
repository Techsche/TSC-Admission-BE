document.addEventListener("DOMContentLoaded", function () {

    const passwordInput = document.getElementById("id_password");
    const passwordToggle = document.getElementById("passwordToggle");
    const eyeIcon = document.getElementById("eyeIcon");
    const loginButton = document.getElementById("loginButton");

    if (passwordToggle && passwordInput) {

        passwordToggle.addEventListener("click", function () {

            const isPassword =
                passwordInput.type === "password";

            passwordInput.type =
                isPassword ? "text" : "password";

            passwordToggle.setAttribute(
                "aria-label",
                isPassword
                    ? "Hide password"
                    : "Show password"
            );

            if (isPassword) {

                eyeIcon.innerHTML = `
                    <path
                        d="M3 3l18 18"
                    />

                    <path
                        d="M10.6 10.6a2 2 0 0 0 2.8 2.8"
                    />

                    <path
                        d="M9.9 5.2A9.8 9.8 0 0 1 12 5
                           c6.5 0 10 7 10 7
                           a17 17 0 0 1-3.1 3.9"
                    />

                    <path
                        d="M6.1 6.1C3.4 8 2 12 2 12
                           s3.5 7 10 7
                           a9.8 9.8 0 0 0 4.1-.9"
                    />
                `;

            } else {

                eyeIcon.innerHTML = `
                    <path
                        d="M2 12s3.5-7 10-7
                           10 7 10 7
                           -3.5 7-10 7S2 12 2 12Z"
                    />

                    <circle
                        cx="12"
                        cy="12"
                        r="3"
                    />
                `;
            }

        });

    }


    /*
     * Small loading state.
     *
     * Django still handles the actual
     * authentication and form submission.
     */
    const form = document.querySelector(".login-form");

    if (form && loginButton) {

        form.addEventListener("submit", function () {

            loginButton.classList.add("loading");

            loginButton.querySelector(".button-text").textContent =
                "Signing in...";

        });

    }

});