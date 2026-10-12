/* =========================================
   VERITEXT — FRONTEND INTERACTIONS
========================================= */

document.addEventListener("DOMContentLoaded", () => {

    /* =====================================
       NAVIGATION
    ===================================== */

    const navLinks = document.querySelectorAll(".nav-links a");

    navLinks.forEach((link) => {

        link.addEventListener("click", () => {

            navLinks.forEach((item) => {
                item.classList.remove("active");
            });

            link.classList.add("active");

        });

    });


    /* =====================================
       ANALYZE BUTTONS
    ===================================== */

    const analyzeButtons = document.querySelectorAll(
        ".primary-button, .nav-button"
    );

    analyzeButtons.forEach((button) => {

        button.addEventListener("click", () => {

            showComingSoon();

        });

    });


    /* =====================================
       EXPLORE ENGINE BUTTON
    ===================================== */

    const exploreButton = document.querySelector(".secondary-button");

    if (exploreButton) {

        exploreButton.addEventListener("click", () => {

            const section = document.querySelector("#how-it-works");

            if (section) {

                section.scrollIntoView({
                    behavior: "smooth"
                });

            }

        });

    }


    /* =====================================
       SCROLL REVEAL
    ===================================== */

    const revealElements = document.querySelectorAll(
        ".process-card, .about-card, .engine-strip"
    );

    const revealObserver = new IntersectionObserver(
        (entries) => {

            entries.forEach((entry) => {

                if (entry.isIntersecting) {

                    entry.target.classList.add("visible");

                    revealObserver.unobserve(entry.target);

                }

            });

        },
        {
            threshold: 0.15
        }
    );


    revealElements.forEach((element) => {

        element.style.opacity = "0";
        element.style.transform = "translateY(30px)";
        element.style.transition =
            "opacity 0.8s ease, transform 0.8s ease";

        revealObserver.observe(element);

    });


    /* =====================================
       MOUSE MOVEMENT — HERO VISUAL
    ===================================== */

    const heroVisual = document.querySelector(".hero-visual");

    if (heroVisual && window.innerWidth > 900) {

        heroVisual.addEventListener("mousemove", (event) => {

            const rect = heroVisual.getBoundingClientRect();

            const x =
                (event.clientX - rect.left) / rect.width - 0.5;

            const y =
                (event.clientY - rect.top) / rect.height - 0.5;


            const card =
                heroVisual.querySelector(".analysis-card");

            if (card) {

                card.style.transform = `
                    translate(${x * 8}px, ${y * 8}px)
                `;

            }

        });


        heroVisual.addEventListener("mouseleave", () => {

            const card =
                heroVisual.querySelector(".analysis-card");

            if (card) {

                card.style.transform = "";

            }

        });

    }


    /* =====================================
       SIMILARITY NUMBER ANIMATION
    ===================================== */

    const similarityNumber =
        document.querySelector(".similarity-heading strong");

    if (similarityNumber) {

        animatePercentage(
            similarityNumber,
            78.17,
            1800
        );

    }


    /* =====================================
       STATUS DOT INTERACTION
    ===================================== */

    const statusDot =
        document.querySelector(".status-dot");

    if (statusDot) {

        setInterval(() => {

            statusDot.classList.toggle("active-pulse");

        }, 2000);

    }

});


/* =========================================
   PERCENTAGE ANIMATION
========================================= */

function animatePercentage(element, target, duration) {

    let startTime = null;


    function update(currentTime) {

        if (!startTime) {
            startTime = currentTime;
        }


        const elapsed = currentTime - startTime;

        const progress =
            Math.min(elapsed / duration, 1);


        /*
            Ease-out animation
        */

        const eased =
            1 - Math.pow(1 - progress, 3);


        const current =
            target * eased;


        element.textContent =
            `${current.toFixed(2)}%`;


        if (progress < 1) {

            requestAnimationFrame(update);

        }

    }


    requestAnimationFrame(update);

}


/* =========================================
   TEMPORARY ANALYZE MESSAGE
========================================= */

function showComingSoon() {

    /*
        This is temporary.

        Later this button will open
        the real plagiarism analysis
        workspace connected to FastAPI.
    */

    const existing =
        document.querySelector(".temporary-notification");

    if (existing) {
        return;
    }


    const notification =
        document.createElement("div");


    notification.className =
        "temporary-notification";


    notification.innerHTML = `
        <div class="notification-icon">✦</div>

        <div>
            <strong>Analysis Workspace</strong>

            <span>
                Upload interface coming next.
            </span>
        </div>
    `;


    document.body.appendChild(notification);


    setTimeout(() => {

        notification.classList.add("show");

    }, 50);


    setTimeout(() => {

        notification.classList.remove("show");

        setTimeout(() => {

            notification.remove();

        }, 400);

    }, 3000);

}


/* =========================================
   TEMPORARY NOTIFICATION STYLE
========================================= */

const notificationStyle =
    document.createElement("style");


notificationStyle.textContent = `

    .temporary-notification {

        position: fixed;

        right: 25px;
        bottom: 25px;

        z-index: 9999;

        display: flex;

        align-items: center;

        gap: 13px;

        min-width: 270px;

        padding: 15px 17px;

        border: 1px solid rgba(141, 245, 194, 0.22);

        border-radius: 12px;

        background: rgba(12, 16, 23, 0.94);

        backdrop-filter: blur(20px);

        box-shadow:
            0 20px 60px rgba(0, 0, 0, 0.45);

        opacity: 0;

        transform:
            translateY(20px)
            scale(0.97);

        transition:
            opacity 0.4s ease,
            transform 0.4s ease;

    }


    .temporary-notification.show {

        opacity: 1;

        transform:
            translateY(0)
            scale(1);

    }


    .notification-icon {

        width: 34px;
        height: 34px;

        display: grid;

        place-items: center;

        border-radius: 9px;

        color: #8df5c2;

        background:
            rgba(141, 245, 194, 0.1);

        font-size: 15px;

    }


    .temporary-notification strong {

        display: block;

        color: #f4f6f8;

        font-family: "Manrope", sans-serif;

        font-size: 11px;

    }


    .temporary-notification span {

        display: block;

        margin-top: 4px;

        color: #68717f;

        font-family: "DM Mono", monospace;

        font-size: 7px;

    }

`;


document.head.appendChild(notificationStyle);
// ==========================================
// VERITEXT BACKEND CONNECTION
// ==========================================

const API_BASE_URL = "http://127.0.0.1:8000";

async function checkBackendConnection() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/health`);

        if (!response.ok) {
            throw new Error("Backend responded with an error");
        }

        const data = await response.json();

        console.log("✓ VeriText backend connected:", data);

        return true;

    } catch (error) {
        console.error("✕ VeriText backend connection failed:", error);

        return false;
    }
}


// Check backend when the frontend loads
document.addEventListener("DOMContentLoaded", () => {
    checkBackendConnection();
});