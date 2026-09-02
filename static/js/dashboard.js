/* =========================================================
   TECHSCHE CAMPUS
   DASHBOARD JAVASCRIPT
========================================================= */

document.addEventListener("DOMContentLoaded", function () {

    /* =====================================================
       STAT NUMBER ANIMATION
    ===================================================== */

    const statValues = document.querySelectorAll("[data-stat-value]");


    function animateNumber(element) {

        const target = parseInt(
            element.getAttribute("data-stat-value"),
            10
        );

        if (isNaN(target)) {
            return;
        }

        const duration = 700;
        const startTime = performance.now();

        function updateNumber(currentTime) {

            const elapsed = currentTime - startTime;

            const progress = Math.min(
                elapsed / duration,
                1
            );

            /*
            Ease-out animation
            */
            const easedProgress =
                1 - Math.pow(1 - progress, 3);

            const currentValue =
                Math.floor(target * easedProgress);

            element.textContent =
                currentValue.toLocaleString("en-IN");

            if (progress < 1) {
                requestAnimationFrame(updateNumber);
            }

        }

        requestAnimationFrame(updateNumber);
    }


    statValues.forEach(function (element) {
        animateNumber(element);
    });


    /* =====================================================
       CHART BAR ANIMATION
    ===================================================== */

    const chartBars = document.querySelectorAll(
        ".chart-bar[data-height]"
    );


    chartBars.forEach(function (bar, index) {

        const height =
            bar.getAttribute("data-height");

        /*
        Start from zero
        */
        bar.style.height = "0%";

        /*
        Animate after a small delay
        */
        setTimeout(function () {

            bar.style.height = height + "%";

        }, 100 + (index * 70));

    });


    /* =====================================================
       CURRENT DATE
    ===================================================== */

    const currentDate =
        document.querySelector("[data-current-date]");


    if (currentDate) {

        const today = new Date();

        const options = {
            day: "2-digit",
            month: "short",
            year: "numeric"
        };

        currentDate.textContent =
            today.toLocaleDateString(
                "en-IN",
                options
            );

    }


    /* =====================================================
       QUICK ACTIONS
    ===================================================== */

    const quickActions =
        document.querySelectorAll(".quick-action");


    quickActions.forEach(function (action) {

        action.addEventListener("click", function () {

            /*
            Navigation is handled by the normal Django
            <a href=""> element.

            This class is only for optional visual feedback.
            */

            action.classList.add("clicked");

            setTimeout(function () {
                action.classList.remove("clicked");
            }, 150);

        });

    });


    /* =====================================================
       DASHBOARD REFRESH
    ===================================================== */

    const refreshButton =
        document.querySelector("[data-dashboard-refresh]");


    if (refreshButton) {

        refreshButton.addEventListener("click", function () {

            refreshButton.classList.add("loading");

            /*
            For now simply reload the dashboard.

            Later this can be changed to fetch dashboard
            statistics through an API without reloading.
            */

            window.location.reload();

        });

    }


    /* =====================================================
       TOOLTIP SUPPORT
    ===================================================== */

    const tooltipElements =
        document.querySelectorAll("[data-tooltip]");


    tooltipElements.forEach(function (element) {

        element.setAttribute(
            "title",
            element.getAttribute("data-tooltip")
        );

    });


});