// Client-side validation for the form
// Prevents submission if required fields are missing or invalid

document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("assignmentForm");

    form.addEventListener("submit", function (event) {
        let valid = true;

        document.querySelectorAll(".error").forEach(error => {
            error.textContent = "";
        });

        const fullName = document.getElementById("full_name").value.trim();
        const email = document.getElementById("email").value.trim();
        const experienceLevel = document.getElementById("experience_level").value;
        const primaryStack = document.getElementById("primary_stack").value;
        const projects = document.getElementById("projects");
        const selectedProjects = Array.from(projects.selectedOptions);
        const preferredDuration = document.querySelector('input[name="preferred_duration"]:checked')

        if (!fullName) {
            document.querySelector("#full_name + .error").textContent = "Full name is required.";
            valid = false;
        }

        if (!email) {
            document.querySelector("#email + .error").textContent = "Email address is required.";
            valid = false;
        } else if (!isValidEmail(email)) {
            document.querySelector("#email + .error").textContent = "Please enter a valid email address.";
            valid = false;
        }

        if (!experienceLevel) {
            document.querySelector("#experience_level + .error").textContent = "Please select your experience level.";
            valid = false;
        }

        if (!primaryStack) {
            document.querySelector("#primary_stack + .error").textContent = "Please select your primary technology stack.";
            valid = false;
        }

        if (selectedProjects.length === 0) {
            document.querySelector("#projects + .error").textContent = "Please select at least one project.";
            valid = false;
        }

        const durationError = document.querySelector('input[name="preferred_duration"]').closest(".form-group").querySelector(".error");
        if (!preferredDuration) {
            durationError.textContent = "Please select preferred project duration.";
            valid = false;
        }

        if (!valid) {
            event.preventDefault();
        }
    });

    function isValidEmail(email) {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    }
});