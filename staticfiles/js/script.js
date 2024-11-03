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

