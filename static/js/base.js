/* =========================================================
   TECHSCHE CAMPUS
   BASE JAVASCRIPT
========================================================= */

document.addEventListener("DOMContentLoaded", function () {

    const sidebar = document.getElementById("sidebar");
    const sidebarOverlay = document.getElementById("sidebarOverlay");
    const sidebarClose = document.getElementById("sidebarClose");

    /*
    ---------------------------------------------------------
    SIDEBAR TOGGLE
    ---------------------------------------------------------
    The header toggle button should have:
        id="sidebarToggle"
    */

    const sidebarToggle = document.getElementById("sidebarToggle");


    /* -----------------------------------------------------
       OPEN SIDEBAR
    ----------------------------------------------------- */

    function openSidebar() {

        if (!sidebar) {
            return;
        }

        sidebar.classList.add("open");

        if (sidebarOverlay) {
            sidebarOverlay.classList.add("active");
            sidebarOverlay.setAttribute("aria-hidden", "false");
        }

        document.body.classList.add("sidebar-open");
    }


    /* -----------------------------------------------------
       CLOSE SIDEBAR
    ----------------------------------------------------- */

    function closeSidebar() {

        if (!sidebar) {
            return;
        }

        sidebar.classList.remove("open");

        if (sidebarOverlay) {
            sidebarOverlay.classList.remove("active");
            sidebarOverlay.setAttribute("aria-hidden", "true");
        }

        document.body.classList.remove("sidebar-open");
    }


    /* -----------------------------------------------------
       TOGGLE BUTTON
    ----------------------------------------------------- */

    if (sidebarToggle) {

        sidebarToggle.addEventListener("click", function () {

            if (sidebar && sidebar.classList.contains("open")) {
                closeSidebar();
            } else {
                openSidebar();
            }

        });

    }


    /* -----------------------------------------------------
       CLOSE BUTTON
    ----------------------------------------------------- */

    if (sidebarClose) {

        sidebarClose.addEventListener("click", function () {
            closeSidebar();
        });

    }


    /* -----------------------------------------------------
       OVERLAY CLICK
    ----------------------------------------------------- */

    if (sidebarOverlay) {

        sidebarOverlay.addEventListener("click", function () {
            closeSidebar();
        });

    }


    /* -----------------------------------------------------
       ESCAPE KEY
    ----------------------------------------------------- */

    document.addEventListener("keydown", function (event) {

        if (event.key === "Escape") {
            closeSidebar();
        }

    });


    /* -----------------------------------------------------
       CLOSE SIDEBAR AFTER NAVIGATION ON MOBILE
    ----------------------------------------------------- */

    if (sidebar) {

        const navLinks = sidebar.querySelectorAll(".nav-item");

        navLinks.forEach(function (link) {

            link.addEventListener("click", function () {

                if (window.innerWidth <= 768) {
                    closeSidebar();
                }

            });

        });

    }


    /* -----------------------------------------------------
       WINDOW RESIZE
    ----------------------------------------------------- */

    let resizeTimer;

    window.addEventListener("resize", function () {

        clearTimeout(resizeTimer);

        resizeTimer = setTimeout(function () {

            if (window.innerWidth > 768) {
                closeSidebar();
            }

        }, 100);

    });


    /* -----------------------------------------------------
       PREVENT BODY SCROLL WHEN SIDEBAR IS OPEN
    ----------------------------------------------------- */

    function updateBodyScroll() {

        if (
            window.innerWidth <= 768 &&
            sidebar &&
            sidebar.classList.contains("open")
        ) {
            document.body.style.overflow = "hidden";
        } else {
            document.body.style.overflow = "";
        }

    }


    /*
    ---------------------------------------------------------
    OBSERVE SIDEBAR CLASS CHANGES
    ---------------------------------------------------------
    */

    if (sidebar) {

        const observer = new MutationObserver(function () {
            updateBodyScroll();
        });

        observer.observe(sidebar, {
            attributes: true,
            attributeFilter: ["class"]
        });

    }


    /* -----------------------------------------------------
       ACTIVE NAVIGATION
       Django already adds the active class server-side,
       so we don't need to calculate it with JavaScript.
    ----------------------------------------------------- */

});