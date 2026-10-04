const jobDescription =
    document.getElementById("jobDescription");

const characterCount =
    document.getElementById("characterCount");

const analyzeButton =
    document.getElementById("analyzeButton");

const loadingState =
    document.getElementById("loadingState");

const errorState =
    document.getElementById("errorState");

const errorMessage =
    document.getElementById("errorMessage");

const resultsSection =
    document.getElementById("results");


/* =========================================
   CHARACTER COUNTER
========================================= */

jobDescription.addEventListener(
    "input",
    () => {

        const length =
            jobDescription.value.length;

        characterCount.textContent =
            `${length} / 30000`;

    }
);


/* =========================================
   HTML ESCAPING
========================================= */

function escapeHtml(value) {

    const div =
        document.createElement("div");

    div.textContent =
        value ?? "";

    return div.innerHTML;
}


/* =========================================
   CREATE TAGS
========================================= */

function createTags(items) {

    if (
        !Array.isArray(items) ||
        items.length === 0
    ) {

        return `
            <span class="empty-result">
                Not specified
            </span>
        `;
    }


    return `
        <div class="result-tags">

            ${items.map(
                item => `
                    <span class="result-tag">
                        ${escapeHtml(item)}
                    </span>
                `
            ).join("")}

        </div>
    `;
}


/* =========================================
   CREATE LIST
========================================= */

function createList(items) {

    if (
        !Array.isArray(items) ||
        items.length === 0
    ) {

        return `
            <p class="empty-result">
                Not specified
            </p>
        `;
    }


    return `
        <ul class="result-list">

            ${items.map(
                item => `
                    <li>
                        ${escapeHtml(item)}
                    </li>
                `
            ).join("")}

        </ul>
    `;
}


/* =========================================
   SHOW ERROR
========================================= */

function showError(message) {

    errorMessage.textContent =
        message;

    errorState.classList.remove(
        "hidden"
    );

    loadingState.classList.add(
        "hidden"
    );
}


/* =========================================
   HIDE ERROR
========================================= */

function hideError() {

    errorState.classList.add(
        "hidden"
    );

    errorMessage.textContent =
        "";
}


/* =========================================
   SHOW LOADING
========================================= */

function showLoading() {

    loadingState.classList.remove(
        "hidden"
    );

    analyzeButton.disabled = true;

    analyzeButton.textContent =
        "Analyzing...";
}


/* =========================================
   HIDE LOADING
========================================= */

function hideLoading() {

    loadingState.classList.add(
        "hidden"
    );

    analyzeButton.disabled = false;

    analyzeButton.textContent =
        "Analyze Job";
}


/* =========================================
   DISPLAY RESULTS
========================================= */

function displayResults(analysis) {

    document.getElementById(
        "resultJobTitle"
    ).textContent =
        analysis.job_title ||
        "Job Analysis";


    document.getElementById(
        "summaryResult"
    ).textContent =
        analysis.summary ||
        "No summary available.";


    document.getElementById(
        "technicalSkillsResult"
    ).innerHTML =
        createTags(
            analysis.technical_skills
        );


    document.getElementById(
        "softSkillsResult"
    ).innerHTML =
        createTags(
            analysis.soft_skills
        );


    document.getElementById(
        "toolsResult"
    ).innerHTML =
        createTags(
            analysis.tools_and_technologies
        );


    document.getElementById(
        "experienceResult"
    ).innerHTML =
        createList(
            analysis.experience
        );


    document.getElementById(
        "educationResult"
    ).innerHTML =
        createList(
            analysis.education
        );


    document.getElementById(
        "prioritySkillsResult"
    ).innerHTML =
        createTags(
            analysis.priority_skills
        );


    document.getElementById(
        "keywordsResult"
    ).innerHTML =
        createTags(
            analysis.important_keywords
        );


    document.getElementById(
        "roadmapResult"
    ).innerHTML =
        createList(
            analysis.learning_roadmap
        );


    document.getElementById(
        "projectsResult"
    ).innerHTML =
        createList(
            analysis.project_ideas
        );


    resultsSection.classList.remove(
        "hidden"
    );


    setTimeout(
        () => {

            resultsSection.scrollIntoView({
                behavior: "smooth",
                block: "start"
            });

        },
        100
    );
}


/* =========================================
   ANALYZE JOB
========================================= */

analyzeButton.addEventListener(
    "click",
    async () => {

        const text =
            jobDescription.value.trim();


        hideError();


        if (text.length < 30) {

            showError(
                "Please provide a job description with at least 30 characters."
            );

            return;
        }


        showLoading();


        try {

            const response =
                await fetch(
                    "/analyze",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body: JSON.stringify({
                            job_description:
                                text
                        })
                    }
                );


            const data =
                await response.json();


            if (
                !response.ok ||
                !data.success
            ) {

                throw new Error(
                    data.error ||
                    "Analysis failed."
                );
            }


            displayResults(
                data.analysis
            );


        } catch (error) {

            console.error(
                "Analysis error:",
                error
            );


            showError(
                error.message ||
                "An unexpected error occurred."
            );


        } finally {

            hideLoading();

        }

    }
);


/* =========================================
   ENTER KEY SUPPORT
========================================= */

jobDescription.addEventListener(
    "keydown",
    event => {

        if (
            event.ctrlKey &&
            event.key === "Enter"
        ) {

            analyzeButton.click();

        }

    }
);