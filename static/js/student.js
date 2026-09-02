document.addEventListener("DOMContentLoaded", function () {
  "use strict";

  /* =====================================================
       ELEMENTS
    ====================================================== */

  const searchInput = document.getElementById("studentSearch");

  const clearSearch = document.getElementById("clearStudentSearch");

  const tableBody = document.getElementById("studentsTableBody");

  const paginationButtons = document.getElementById("paginationButtons");

  const pagination = document.getElementById("studentsPagination");

  const loading = document.getElementById("studentsLoading");

  const empty = document.getElementById("studentsEmpty");

  const emptyTitle = document.getElementById("studentsEmptyTitle");

  const emptyMessage = document.getElementById("studentsEmptyMessage");

  const studentCount = document.getElementById("studentCount");

  const paginationStart = document.getElementById("paginationStart");

  const paginationEnd = document.getElementById("paginationEnd");

  const paginationTotal = document.getElementById("paginationTotal");

  /* =====================================================
       STATE
    ====================================================== */

  let searchTimer = null;

  let currentRequest = null;

  let isLoading = false;

  /* =====================================================
       SAFETY CHECK
    ====================================================== */

  if (!searchInput || !tableBody) {
    console.error("Students page elements could not be found.");

    return;
  }

  /* =====================================================
       LOAD STUDENTS
    ====================================================== */

  function loadStudents(page = 1) {
    const search = searchInput.value.trim();

    page = parseInt(page, 10) || 1;

    showLoading();

    const params = new URLSearchParams();

    params.set("page", page);

    if (search) {
      params.set("search", search);
    }

    /*
     * Abort previous request if the user searches
     * again before the previous request finishes.
     */

    if (currentRequest) {
      currentRequest.abort();
    }

    currentRequest = new AbortController();

    fetch(`${window.location.pathname}?${params.toString()}`, {
      method: "GET",

      headers: {
        "X-Requested-With": "XMLHttpRequest",
        Accept: "application/json",
      },

      signal: currentRequest.signal,
    })
      .then(function (response) {
        if (!response.ok) {
          throw new Error(`HTTP error: ${response.status}`);
        }

        return response.json();
      })

      .then(function (data) {
        /*
         * Update table
         */

        tableBody.innerHTML = data.html || "";

        /*
         * Update counters
         */

        updateCounters(data);

        /*
         * Update pagination
         */

        renderPagination(data);

        /*
         * Update empty state
         */

        updateEmptyState(Number(data.total || 0), search);

        /*
         * Update clear button
         */

        updateClearButton();

        /*
         * Update browser URL
         */

        const newUrl = `${window.location.pathname}?${params.toString()}`;

        window.history.replaceState({}, "", newUrl);

        /*
         * Make sure dynamically inserted
         * action buttons work.
         */

        initializeDynamicRows();
      })

      .catch(function (error) {
        /*
         * Ignore aborted requests.
         */

        if (error.name === "AbortError") {
          return;
        }

        console.error("Unable to load students:", error);

        /*
         * Show error inside table.
         */

        tableBody.innerHTML = `
                <tr>
                    <td colspan="10">
                        <div class="table-empty">
                            Unable to load students.
                            Please try again.
                        </div>
                    </td>
                </tr>
            `;

        /*
         * Hide normal empty state
         * because this is an error.
         */

        if (empty) {
          empty.hidden = true;
        }

        if (pagination) {
          pagination.hidden = true;
        }
      })

      .finally(function () {
        currentRequest = null;

        hideLoading();
      });
  }

  /* =====================================================
       UPDATE COUNTERS
    ====================================================== */

  function updateCounters(data) {
    const total = Number(data.total || 0);

    if (studentCount) {
      studentCount.textContent = total;
    }

    if (paginationTotal) {
      paginationTotal.textContent = total;
    }

    if (paginationStart) {
      paginationStart.textContent = Number(data.start || 0);
    }

    if (paginationEnd) {
      paginationEnd.textContent = Number(data.end || 0);
    }
  }

  /* =====================================================
       SEARCH
    ====================================================== */

  searchInput.addEventListener("input", function () {
    updateClearButton();

    clearTimeout(searchTimer);

    searchTimer = setTimeout(function () {
      loadStudents(1);
    }, 350);
  });

  /* =====================================================
       CLEAR SEARCH
    ====================================================== */

  if (clearSearch) {
    clearSearch.addEventListener("click", function () {
      searchInput.value = "";

      updateClearButton();

      searchInput.focus();

      loadStudents(1);
    });
  }

  /* =====================================================
       PAGINATION
    ====================================================== */

  if (paginationButtons) {
    paginationButtons.addEventListener("click", function (event) {
      const button = event.target.closest(".students-page-btn");

      if (!button) {
        return;
      }

      const page = parseInt(button.dataset.page, 10);

      if (!page || button.disabled) {
        return;
      }

      loadStudents(page);

      /*
       * Scroll to students card.
       */

      const card = document.querySelector(".students-card");

      if (card) {
        card.scrollIntoView({
          behavior: "smooth",
          block: "start",
        });
      }
    });
  }

  /* =====================================================
       DELETE STUDENT
    ====================================================== */

  tableBody.addEventListener("click", function (event) {
    const deleteButton = event.target.closest(".delete-student");

    if (!deleteButton) {
      return;
    }

    const studentName = deleteButton.dataset.name || "this student";

    const deleteUrl = deleteButton.dataset.deleteUrl;

    if (!deleteUrl) {
      console.error("Delete URL is missing.");

      alert("Unable to delete student.");

      return;
    }

    /*
     * Confirmation
     */

    const confirmed = window.confirm(
      `Are you sure you want to delete ${studentName}?`,
    );

    if (!confirmed) {
      return;
    }

    deleteStudent(deleteUrl, deleteButton);
  });

  /* =====================================================
       ACTIVE / INACTIVE TOGGLE
    ====================================================== */

  tableBody.addEventListener("click", function (event) {
    const toggle = event.target.closest(".active-toggle");

    if (!toggle) {
      return;
    }

    const toggleUrl = toggle.dataset.toggleUrl;

    if (!toggleUrl) {
      console.error("Toggle URL is missing.");

      return;
    }

    const currentActive = toggle.dataset.active === "true";

    /*
     * Disable while request is running.
     */

    toggle.disabled = true;

    fetch(toggleUrl, {
      method: "POST",

      headers: {
        "X-Requested-With": "XMLHttpRequest",
        "X-CSRFToken": getCsrfToken(),
        Accept: "application/json",
      },
    })
      .then(function (response) {
        if (!response.ok) {
          throw new Error(`HTTP error: ${response.status}`);
        }

        return response.json();
      })

      .then(function (data) {
        if (!data.success) {
          throw new Error(data.message || "Unable to update status.");
        }

        const isActive = Boolean(data.is_active);

        toggle.dataset.active = isActive ? "true" : "false";

        toggle.classList.toggle("active", isActive);
      })

      .catch(function (error) {
        console.error("Unable to update active status:", error);

        /*
         * Restore original state.
         */

        toggle.dataset.active = currentActive ? "true" : "false";

        toggle.classList.toggle("active", currentActive);

        alert("Unable to update student status. Please try again.");
      })

      .finally(function () {
        toggle.disabled = false;
      });
  });

  /* =====================================================
       DELETE FUNCTION
    ====================================================== */

  function deleteStudent(deleteUrl, deleteButton) {
    /*
     * Disable button immediately.
     */

    deleteButton.disabled = true;

    deleteButton.style.pointerEvents = "none";

    showLoading();

    fetch(deleteUrl, {
      method: "POST",

      headers: {
        "X-Requested-With": "XMLHttpRequest",
        "X-CSRFToken": getCsrfToken(),
        Accept: "application/json",
      },
    })
      .then(function (response) {
        if (!response.ok) {
          throw new Error(`HTTP error: ${response.status}`);
        }

        return response.json();
      })

      .then(function (data) {
        if (!data.success) {
          throw new Error(data.message || "Unable to delete student.");
        }

        /*
         * Reload current page.
         */

        let currentPage = getCurrentPage();

        /*
         * If this was the last row on the page,
         * move to previous page.
         *
         * Example:
         *
         * Page 3 has one student.
         * Delete it.
         * Automatically load page 2.
         */

        const rows = tableBody.querySelectorAll("tr");

        if (rows.length <= 1 && currentPage > 1) {
          currentPage--;
        }

        loadStudents(currentPage);
      })

      .catch(function (error) {
        console.error("Delete error:", error);

        alert(error.message || "Unable to delete student. Please try again.");

        hideLoading();

        deleteButton.disabled = false;

        deleteButton.style.pointerEvents = "";
      });
  }

  /* =====================================================
       RENDER PAGINATION
    ====================================================== */

  function renderPagination(data) {
    if (!paginationButtons) {
      return;
    }

    paginationButtons.innerHTML = "";

    /*
     * No records
     */

    if (!data.total || Number(data.total) === 0) {
      if (pagination) {
        pagination.hidden = true;
      }

      return;
    }

    /*
     * Previous
     */

    if (data.has_previous) {
      addPageButton(data.previous_page, "‹", false, "Previous page");
    }

    /*
     * Page numbers
     */

    if (Array.isArray(data.pages)) {
      data.pages.forEach(function (page) {
        /*
         * Ellipsis
         */

        if (page === "...") {
          const dots = document.createElement("span");

          dots.className = "students-pagination-dots";

          dots.textContent = "…";

          paginationButtons.appendChild(dots);

          return;
        }

        /*
         * Page button
         */

        addPageButton(page, page, Number(page) === Number(data.current_page));
      });
    }

    /*
     * Next
     */

    if (data.has_next) {
      addPageButton(data.next_page, "›", false, "Next page");
    }
  }

  /* =====================================================
       ADD PAGE BUTTON
    ====================================================== */

  function addPageButton(page, text, active = false, label = "") {
    const button = document.createElement("button");

    button.type = "button";

    button.className = "students-page-btn";

    if (active) {
      button.classList.add("active");

      button.setAttribute("aria-current", "page");
    }

    button.dataset.page = page;

    button.textContent = text;

    if (label) {
      button.setAttribute("aria-label", label);
    }

    paginationButtons.appendChild(button);
  }

  /* =====================================================
       EMPTY STATE
    ====================================================== */

  function updateEmptyState(total, search) {
    if (!empty) {
      return;
    }

    total = Number(total) || 0;

    if (total === 0) {
      empty.hidden = false;

      if (search) {
        if (emptyTitle) {
          emptyTitle.textContent = "No results found";
        }

        if (emptyMessage) {
          emptyMessage.textContent =
            "No students match your search. Try a different search term.";
        }
      } else {
        if (emptyTitle) {
          emptyTitle.textContent = "No students found";
        }

        if (emptyMessage) {
          emptyMessage.textContent = "There are no student applications yet.";
        }
      }

      if (pagination) {
        pagination.hidden = true;
      }
    } else {
      empty.hidden = true;

      if (pagination) {
        pagination.hidden = false;
      }
    }
  }

  /* =====================================================
       CLEAR SEARCH BUTTON
    ====================================================== */

  function updateClearButton() {
    if (!clearSearch) {
      return;
    }

    if (searchInput.value.trim()) {
      clearSearch.classList.add("visible");
    } else {
      clearSearch.classList.remove("visible");
    }
  }

  /* =====================================================
       LOADING
    ====================================================== */

  function showLoading() {
    isLoading = true;

    if (loading) {
      loading.hidden = false;
    }
  }

  function hideLoading() {
    isLoading = false;

    if (loading) {
      loading.hidden = true;
    }
  }

  /* =====================================================
       CURRENT PAGE
    ====================================================== */

  function getCurrentPage() {
    const params = new URLSearchParams(window.location.search);

    const page = parseInt(params.get("page") || "1", 10);

    return page > 0 ? page : 1;
  }

  /* =====================================================
       CSRF TOKEN
    ====================================================== */

  function getCsrfToken() {
    /*
     * First try Django's csrftoken cookie.
     */

    const name = "csrftoken=";

    const cookies = document.cookie.split(";");

    for (let cookie of cookies) {
      cookie = cookie.trim();

      if (cookie.startsWith(name)) {
        return decodeURIComponent(cookie.substring(name.length));
      }
    }

    /*
     * Fallback:
     * Look for csrfmiddlewaretoken
     * in the page.
     */

    const csrfInput = document.querySelector("[name=csrfmiddlewaretoken]");

    if (csrfInput) {
      return csrfInput.value;
    }

    return "";
  }

  /* =====================================================
       DYNAMIC ROW INITIALIZATION
    ====================================================== */

  function initializeDynamicRows() {
    /*
     * This function intentionally does not
     * attach click handlers.
     *
     * The table uses event delegation,
     * so newly loaded AJAX rows work automatically.
     */

    const rows = tableBody.querySelectorAll("tr");

    rows.forEach(function (row) {
      row.classList.add("student-row");
    });
  }

  /* =====================================================
       INITIAL STATE
    ====================================================== */

  updateClearButton();

  /*
   * Read initial count from Django.
   */

  const initialTotal =
    parseInt(studentCount ? studentCount.textContent.trim() : "0", 10) || 0;

  /*
   * Initialize empty state.
   */

  updateEmptyState(initialTotal, searchInput.value.trim());

  /*
   * Initialize rows.
   */

  initializeDynamicRows();

  /*
   * Make sure loader starts hidden.
   */

  hideLoading();
});
