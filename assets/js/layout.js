document.addEventListener('DOMContentLoaded', () => {
    const sidebar = document.getElementById('sidebar');
    const sidebarToggleBtn = document.getElementById('sidebarToggleBtn');
    const inventoryToggle = document.getElementById('inventoryToggle');
    
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const sidebarOverlay = document.getElementById('sidebarOverlay');
    
    // Toggle Sidebar
    if (sidebarToggleBtn && sidebar) {
        sidebarToggleBtn.addEventListener('click', () => {
            // On desktop, toggle 'collapsed' class
            if (window.innerWidth > 768) {
                sidebar.classList.toggle('collapsed');
                
                // Close dropdowns when collapsing
                if (sidebar.classList.contains('collapsed')) {
                    document.querySelectorAll('.nav-item.open').forEach(item => {
                        item.classList.remove('open');
                    });
                }
            } else {
                // On mobile, toggle 'open' class for off-canvas
                sidebar.classList.toggle('open');
                if (sidebarOverlay) sidebarOverlay.classList.toggle('active');
            }
        });
    }

    // Mobile Menu Button
    if (mobileMenuBtn && sidebar) {
        mobileMenuBtn.addEventListener('click', () => {
            sidebar.classList.add('open');
            if (sidebarOverlay) sidebarOverlay.classList.add('active');
        });
    }

    // Sidebar Overlay Click
    if (sidebarOverlay && sidebar) {
        sidebarOverlay.addEventListener('click', () => {
            sidebar.classList.remove('open');
            sidebarOverlay.classList.remove('active');
        });
    }

    // Toggle Dropdown for Inventory Management
    if (inventoryToggle) {
        inventoryToggle.addEventListener('click', (e) => {
            e.preventDefault();
            
            // Don't toggle if sidebar is collapsed on desktop
            if (window.innerWidth > 768 && sidebar.classList.contains('collapsed')) {
                return;
            }
            
            const parentLi = inventoryToggle.closest('.nav-item');
            if (parentLi) {
                parentLi.classList.toggle('open');
            }
        });
    }

    // Handle Active State for Submenus
    const dropdownLinks = document.querySelectorAll('.dropdown-link');
    dropdownLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            // Only block navigation for placeholder '#' links
            if (link.getAttribute('href') === '#') {
                e.preventDefault();
            }
            // Remove active class from all
            dropdownLinks.forEach(l => l.classList.remove('active'));
            // Add active class to clicked link
            link.classList.add('active');
        });
    });

    // Navbar Dropdowns
    const notificationBtn = document.getElementById('notificationBtn');
    const notificationDropdown = document.getElementById('notificationDropdown');
    const userProfileBtn = document.getElementById('userProfileBtn');
    const profileDropdown = document.getElementById('profileDropdown');

    if (notificationBtn && notificationDropdown) {
        notificationBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            if (profileDropdown) profileDropdown.classList.remove('active');
            if (userProfileBtn) userProfileBtn.classList.remove('active');
            notificationDropdown.classList.toggle('active');
        });
    }

    const closeNotifBtn = document.getElementById('closeNotifBtn');
    if (closeNotifBtn && notificationDropdown) {
        closeNotifBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            notificationDropdown.classList.remove('active');
        });
    }

    if (userProfileBtn && profileDropdown) {
        userProfileBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            if (notificationDropdown) notificationDropdown.classList.remove('active');
            userProfileBtn.classList.toggle('active');
            profileDropdown.classList.toggle('active');
        });
    }

    // Close dropdowns on clicking outside
    window.addEventListener('click', () => {
        if (notificationDropdown) notificationDropdown.classList.remove('active');
        if (profileDropdown) profileDropdown.classList.remove('active');
        if (userProfileBtn) userProfileBtn.classList.remove('active');
    });

    // Prevent closing when clicking inside dropdown
    if (notificationDropdown) {
        notificationDropdown.addEventListener('click', (e) => {
            e.stopPropagation();
        });
    }
    if (profileDropdown) {
        profileDropdown.addEventListener('click', (e) => {
            e.stopPropagation();
        });
    }

    // Handle responsive behavior on window resize
    window.addEventListener('resize', () => {
        if (window.innerWidth <= 768) {
            if (sidebar) {
                sidebar.classList.remove('collapsed');
            }
        } else {
            if (sidebar) {
                sidebar.classList.remove('open');
                if (sidebarOverlay) sidebarOverlay.classList.remove('active');
            }
        }
    });
});
