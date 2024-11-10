document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("sidebarCollapse").addEventListener("click", function () {
        document.getElementById("sidebar").classList.toggle("active");
    });
});

console.log("run from th js django ")
document.addEventListener('DOMContentLoaded', function() {
    const sidebar = document.getElementById('sidebar');
    const sidebarCollapse = document.getElementById('sidebarCollapse');

    console.log('Sidebar Collapse Button:', sidebarCollapse);

    // Toggle sidebar state
    sidebarCollapse.addEventListener('click', function() {
        console.log('Sidebar Collapse Button Clicked');
        sidebar.classList.toggle('minimized');
    });
});




    function handleLoading(button) {
        // Add loading state only if it's not already loading
        if (!button.classList.contains('is-loading')) {
            button.classList.add('is-loading');
            button.disabled = true; // Disable to prevent double-clicking

            // Optional: Show spinner and change text to indicate loading
            button.innerHTML = '<span class="spinner"></span> جاري الحفظ ....';
        }

        // Allow form submission to proceed if this is a form button
        return true; // This ensures that form submission is not blocked
    }

// document.addEventListener('DOMContentLoaded', function () {
//     // Find all forms with submit buttons
//     const forms = document.querySelectorAll('form');
//
//     forms.forEach(form => {
//         // Attach the submit event to each form
//         form.addEventListener('submit', function (event) {
//             const submitButton = form.querySelector('.action-button');
//
//             // If the submit button is found and not already in loading state
//             if (submitButton && !submitButton.classList.contains('is-loading')) {
//                 submitButton.classList.add('is-loading');
//                 submitButton.disabled = true; // Disable the button to prevent double-clicking
//
//                 // Optional: Show spinner and change text to indicate loading
//                 submitButton.innerHTML = '<span class="spinner"></span> Loading...';
//             }
//
//             // The form will continue to submit naturally, without needing return false
//         });
//     });
// });


    document.addEventListener('DOMContentLoaded', function () {
    const forms = document.querySelectorAll('form');

    forms.forEach(form => {
        form.addEventListener('submit', function (event) {
            // Display the full-page loading overlay
            document.getElementById('loading-overlay').style.display = 'flex';
        });
    });
});
