document.addEventListener("DOMContentLoaded", () => {
    "use strict";

    const searchInput = document.getElementById("studentSearch");
    const clearSearch = document.getElementById("clearStudentSearch");

    const tableBody = document.getElementById("studentsTableBody");
    const pagination = document.getElementById("studentsPagination");
    const paginationButtons = document.getElementById("paginationButtons");

    const studentCount = document.getElementById("studentCount");

    const paginationStart = document.getElementById("paginationStart");
    const paginationEnd = document.getElementById("paginationEnd");
    const paginationTotal = document.getElementById("paginationTotal");

    const loading = document.getElementById("studentsLoading");
    const emptyState = document.getElementById("studentsEmpty");
    const emptyTitle = document.getElementById("studentsEmptyTitle");
    const emptyMessage = document.getElementById("studentsEmptyMessage");

    let searchTimer = null;
    let isLoading = false;


    /* =========================================================
       GET CURRENT SEARCH
    ========================================================= */

    function getSearchValue() {
        return searchInput
            ? searchInput.value.trim()
            : "";
    }


    /* =========================================================
       BUILD URL
    ========================================================= */

    function buildUrl(page = 1) {
        const url = new URL(window.location.href);

        const search = getSearchValue();

        if (search) {
            url.searchParams.set("search", search);
        } else {
            url.searchParams.delete("search");
        }

        if (page && Number(page) > 1) {
            url.searchParams.set("page", page);
        } else {
            url.searchParams.delete("page");
        }

        return url;
    }


    /* =========================================================
       UPDATE BROWSER URL
    ========================================================= */

    function updateBrowserUrl(url) {
        window.history.pushState(
            {
                page: url.searchParams.get("page") || "1",
                search: url.searchParams.get("search") || ""
            },
            "",
            url.pathname + url.search
        );
    }


    /* =========================================================
       SHOW / HIDE LOADING
    ========================================================= */

    function showLoading() {
        isLoading = true;

        if (loading) {
            loading.hidden = false;
        }

        document.body.classList.add("students-is-loading");
    }


    function hideLoading() {
        isLoading = false;

        if (loading) {
            loading.hidden = true;
        }

        document.body.classList.remove("students-is-loading");
    }


    /* =========================================================
       UPDATE CLEAR BUTTON
    ========================================================= */

    function updateClearButton() {
        if (!clearSearch || !searchInput) {
            return;
        }

        clearSearch.hidden = searchInput.value.trim() === "";
    }


    /* =========================================================
       UPDATE EMPTY STATE
    ========================================================= */

    function updateEmptyState(total, hasSearch) {
        if (!emptyState) {
            return;
        }

        const isEmpty = Number(total) === 0;

        emptyState.hidden = !isEmpty;

        if (isEmpty) {
            if (emptyTitle) {
                emptyTitle.textContent = hasSearch
                    ? "No results found"
                    : "No students found";
            }

            if (emptyMessage) {
                emptyMessage.textContent = hasSearch
                    ? "No students match your search. Try a different search term."
                    : "There are no student applications yet.";
            }
        }
    }


    /* =========================================================
       UPDATE COUNTERS
    ========================================================= */

    function updateCounters(total, start, end) {
        if (studentCount) {
            studentCount.textContent = total;
        }

        if (paginationStart) {
            paginationStart.textContent = start;
        }

        if (paginationEnd) {
            paginationEnd.textContent = end;
        }

        if (paginationTotal) {
            paginationTotal.textContent = total;
        }
    }


    /* =========================================================
       LOAD STUDENTS
       
       IMPORTANT:
       response.text()
       NOT response.json()
    ========================================================= */

    async function loadStudents(page = 1, updateHistory = true) {

        if (isLoading) {
            return;
        }

        const url = buildUrl(page);

        showLoading();

        try {
            const response = await fetch(url.toString(), {
                method: "GET",

                headers: {
                    "X-Requested-With": "XMLHttpRequest"
                },

                credentials: "same-origin"
            });


            if (!response.ok) {
                throw new Error(
                    `HTTP ${response.status}: ${response.statusText}`
                );
            }


            /*
             * Django is returning HTML.
             *
             * DO NOT use:
             *
             * response.json()
             *
             * because the response contains:
             * <tr>...</tr>
             */

            const html = await response.text();


            /*
             * Parse returned HTML
             */

            const parser = new DOMParser();

            const doc = parser.parseFromString(
                html,
                "text/html"
            );


            /*
             * Get returned elements
             */

            const newTableBody =
                doc.getElementById("studentsTableBody");

            const newPagination =
                doc.getElementById("studentsPagination");

            const newPaginationButtons =
                doc.getElementById("paginationButtons");

            const newStudentCount =
                doc.getElementById("studentCount");

            const newPaginationStart =
                doc.getElementById("paginationStart");

            const newPaginationEnd =
                doc.getElementById("paginationEnd");

            const newPaginationTotal =
                doc.getElementById("paginationTotal");

            const newEmptyState =
                doc.getElementById("studentsEmpty");


            /*
             * Make sure Django returned the expected HTML
             */

            if (!newTableBody) {
                console.error("Returned HTML:");

                console.error(html);

                throw new Error(
                    "studentsTableBody was not found in the response."
                );
            }


            /*
             * Replace table rows
             */

            if (tableBody) {
                tableBody.innerHTML =
                    newTableBody.innerHTML;
            }


            /*
             * Replace pagination buttons
             */

            if (
                paginationButtons &&
                newPaginationButtons
            ) {
                paginationButtons.innerHTML =
                    newPaginationButtons.innerHTML;
            }


            /*
             * Update pagination visibility
             */

            if (pagination) {

                if (newPagination) {
                    pagination.hidden =
                        newPagination.hidden;
                } else {
                    pagination.hidden = true;
                }
            }


            /*
             * Update student count
             */

            if (
                studentCount &&
                newStudentCount
            ) {
                studentCount.textContent =
                    newStudentCount.textContent.trim();
            }


            /*
             * Update pagination counters
             */

            if (
                paginationStart &&
                newPaginationStart
            ) {
                paginationStart.textContent =
                    newPaginationStart.textContent.trim();
            }


            if (
                paginationEnd &&
                newPaginationEnd
            ) {
                paginationEnd.textContent =
                    newPaginationEnd.textContent.trim();
            }


            if (
                paginationTotal &&
                newPaginationTotal
            ) {
                paginationTotal.textContent =
                    newPaginationTotal.textContent.trim();
            }


            /*
             * Update empty state
             */

            if (emptyState && newEmptyState) {

                emptyState.hidden =
                    newEmptyState.hidden;

                if (emptyTitle) {

                    const returnedTitle =
                        newEmptyState.querySelector(
                            "#studentsEmptyTitle"
                        );

                    if (returnedTitle) {
                        emptyTitle.textContent =
                            returnedTitle.textContent.trim();
                    }
                }


                if (emptyMessage) {

                    const returnedMessage =
                        newEmptyState.querySelector(
                            "#studentsEmptyMessage"
                        );

                    if (returnedMessage) {
                        emptyMessage.textContent =
                            returnedMessage.textContent.trim();
                    }
                }
            }


            /*
             * Get total number of students
             */

            let total = 0;

            if (newPaginationTotal) {
                total = parseInt(
                    newPaginationTotal.textContent.trim(),
                    10
                ) || 0;
            }


            /*
             * Update empty state safely
             */

            updateEmptyState(
                total,
                getSearchValue() !== ""
            );


            /*
             * Update browser URL
             *
             * This is what changes:
             *
             * /students/
             *
             * to:
             *
             * /students/?page=2
             */

            if (updateHistory) {
                updateBrowserUrl(url);
            }


            /*
             * Update search clear button
             */

            updateClearButton();


            /*
             * Reinitialize dynamic row state
             */

            initializeDynamicRows();

        } catch (error) {

            console.error(
                "Unable to load students:",
                error
            );

            /*
             * IMPORTANT:
             * Do not replace the current table with
             * an error unless necessary.
             */

            alert(
                "Unable to load students. Please try again."
            );

        } finally {

            hideLoading();
        }
    }


    /* =========================================================
       SEARCH
    ========================================================= */

    if (searchInput) {

        searchInput.addEventListener(
            "input",
            () => {

                updateClearButton();

                clearTimeout(searchTimer);

                searchTimer = setTimeout(
                    () => {

                        loadStudents(
                            1,
                            true
                        );

                    },
                    350
                );
            }
        );


        /*
         * Press Enter
         */

        searchInput.addEventListener(
            "keydown",
            (event) => {

                if (event.key === "Enter") {

                    event.preventDefault();

                    clearTimeout(searchTimer);

                    loadStudents(
                        1,
                        true
                    );
                }
            }
        );
    }


    /* =========================================================
       CLEAR SEARCH
    ========================================================= */

    if (clearSearch) {

        clearSearch.addEventListener(
            "click",
            () => {

                if (searchInput) {
                    searchInput.value = "";
                }

                updateClearButton();

                loadStudents(
                    1,
                    true
                );
            }
        );
    }


    /* =========================================================
       PAGINATION
    ========================================================= */

    if (paginationButtons) {

        paginationButtons.addEventListener(
            "click",
            (event) => {

                const button =
                    event.target.closest(
                        ".students-page-btn"
                    );


                if (!button) {
                    return;
                }


                const page =
                    parseInt(
                        button.dataset.page,
                        10
                    );


                if (!page || isNaN(page)) {
                    return;
                }


                event.preventDefault();


                loadStudents(
                    page,
                    true
                );
            }
        );
    }


    /* =========================================================
       BROWSER BACK / FORWARD
    ========================================================= */

    window.addEventListener(
        "popstate",
        () => {

            const url =
                new URL(window.location.href);


            const page =
                parseInt(
                    url.searchParams.get("page") || "1",
                    10
                );


            const search =
                url.searchParams.get("search") || "";


            if (searchInput) {
                searchInput.value = search;
            }


            updateClearButton();


            /*
             * false = don't push another history entry
             */

            loadStudents(
                page,
                false
            );
        }
    );


    /* =========================================================
       DELETE STUDENT
    ========================================================= */

    if (tableBody) {

        tableBody.addEventListener(
            "click",
            async (event) => {

                const deleteButton =
                    event.target.closest(
                        "[data-delete-student]"
                    );


                if (!deleteButton) {
                    return;
                }


                event.preventDefault();


                const studentId =
                    deleteButton.dataset.deleteStudent;


                if (!studentId) {
                    return;
                }


                const confirmed =
                    window.confirm(
                        "Are you sure you want to delete this student?"
                    );


                if (!confirmed) {
                    return;
                }


                await deleteStudent(
                    studentId
                );
            }
        );
    }


    /* =========================================================
       ACTIVE / INACTIVE TOGGLE
    ========================================================= */

    if (tableBody) {

        tableBody.addEventListener(
            "change",
            async (event) => {

                const toggle =
                    event.target.closest(
                        "[data-toggle-active]"
                    );


                if (!toggle) {
                    return;
                }


                const studentId =
                    toggle.dataset.toggleActive;


                if (!studentId) {
                    return;
                }


                await toggleStudentActive(
                    studentId,
                    toggle.checked
                );
            }
        );
    }


    /* =========================================================
       DELETE REQUEST
    ========================================================= */

    async function deleteStudent(studentId) {

        try {

            const response =
                await fetch(
                    `/students/${studentId}/delete/`,
                    {
                        method: "POST",

                        headers: {
                            "X-CSRFToken": getCsrfToken(),
                            "X-Requested-With": "XMLHttpRequest",
                            "Content-Type": "application/json"
                        },

                        credentials: "same-origin"
                    }
                );


            const data =
                await response.json();


            if (!response.ok || !data.success) {

                throw new Error(
                    data.message ||
                    "Unable to delete student."
                );
            }


            /*
             * Reload current page.
             */

            const currentPage =
                getCurrentPage();


            const currentRows =
                tableBody
                    ? tableBody.querySelectorAll("tr").length
                    : 0;


            /*
             * If last row of current page was deleted,
             * go to previous page.
             */

            let pageToLoad = currentPage;

            if (
                currentRows <= 1 &&
                currentPage > 1
            ) {
                pageToLoad =
                    currentPage - 1;
            }


            await loadStudents(
                pageToLoad,
                true
            );


        } catch (error) {

            console.error(
                "Unable to delete student:",
                error
            );

            alert(
                error.message ||
                "Unable to delete student."
            );
        }
    }


    /* =========================================================
       ACTIVE / INACTIVE REQUEST
    ========================================================= */

    async function toggleStudentActive(
        studentId,
        isActive
    ) {

        try {

            const response =
                await fetch(
                    `/students/${studentId}/toggle-active/`,
                    {
                        method: "POST",

                        headers: {
                            "X-CSRFToken": getCsrfToken(),
                            "X-Requested-With": "XMLHttpRequest",
                            "Content-Type": "application/json"
                        },

                        credentials: "same-origin",

                        body: JSON.stringify({
                            is_active: isActive
                        })
                    }
                );


            const data =
                await response.json();


            if (!response.ok || !data.success) {

                throw new Error(
                    data.message ||
                    "Unable to update student status."
                );
            }


        } catch (error) {

            console.error(
                "Unable to update student status:",
                error
            );


            alert(
                error.message ||
                "Unable to update student status."
            );


            /*
             * Revert checkbox if request failed.
             */

            const checkbox =
                tableBody?.querySelector(
                    `[data-toggle-active="${studentId}"]`
                );


            if (checkbox) {
                checkbox.checked =
                    !isActive;
            }
        }
    }


    /* =========================================================
       GET CURRENT PAGE
    ========================================================= */

    function getCurrentPage() {

        const url =
            new URL(window.location.href);


        return parseInt(
            url.searchParams.get("page") || "1",
            10
        );
    }


    /* =========================================================
       CSRF TOKEN
    ========================================================= */

    function getCsrfToken() {

        const cookie =
            document.cookie
                .split("; ")
                .find(
                    row =>
                        row.startsWith("csrftoken=")
                );


        if (!cookie) {
            return "";
        }


        return decodeURIComponent(
            cookie.split("=")[1]
        );
    }


    /* =========================================================
       DYNAMIC ROW INITIALIZATION
    ========================================================= */

    function initializeDynamicRows() {

        /*
         * Keep this function even if your rows currently
         * don't need initialization.
         *
         * Any future row-specific JS can be added here.
         */

    }


    /* =========================================================
       INITIAL STATE
    ========================================================= */

    updateClearButton();

    initializeDynamicRows();

});