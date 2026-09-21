const API_URL = "http://127.0.0.1:8000/status";

let isFetching = false;


function setText(id, value) {

    const element = document.getElementById(id);

    if (element) {
        element.textContent = value;
    }
}


function setWidth(id, value) {

    const element = document.getElementById(id);

    if (element) {
        element.style.width = value + "%";
    }
}


function updateBattery(data) {

    const battery =
        Math.max(0, Math.min(100, Number(data.battery) || 0));

    const batteryRounded =
        Math.round(battery);


    setText(
        "batteryPercent",
        batteryRounded
    );


    setText(
        "batteryPressure",
        String(data.battery_pressure || "NORMAL").toUpperCase()
    );


    setText(
        "remainingTime",
        data.estimated_remaining_time || "--"
    );


    setWidth(
        "batteryFill",
        battery
    );


    const circle =
        document.querySelector(".battery-circle");


    if (circle) {

        const color =
            battery <= 10
                ? "#d47b6f"
                : battery <= 25
                    ? "#d4a86a"
                    : "#9caf88";


        const degrees =
            battery * 3.6;


        circle.style.background =
            `conic-gradient(
                ${color} 0deg,
                ${color} ${degrees}deg,
                #20261f ${degrees}deg,
                #20261f 360deg
            )`;
    }


    const badge =
        document.getElementById("batteryPressure");


    if (badge) {

        const pressure =
            String(
                data.battery_pressure || "NORMAL"
            ).toLowerCase();


        if (pressure.includes("critical")) {

            badge.style.color = "#d47b6f";
            badge.style.borderColor =
                "rgba(212,123,111,0.3)";
            badge.style.background =
                "rgba(212,123,111,0.08)";

        } else if (pressure.includes("high")) {

            badge.style.color = "#d4a86a";
            badge.style.borderColor =
                "rgba(212,168,106,0.3)";
            badge.style.background =
                "rgba(212,168,106,0.08)";

        } else {

            badge.style.color = "#9caf88";
            badge.style.borderColor =
                "rgba(156,175,136,0.3)";
            badge.style.background =
                "rgba(156,175,136,0.08)";
        }
    }
}


function updateSystem(data) {

    setText(
        "liveCPU",
        `${Number(data.cpu || 0).toFixed(1)}%`
    );


    setText(
        "liveRAM",
        `${Number(data.ram || 0).toFixed(1)}%`
    );


    const workload =
        data.workload || "Light";


    setText(
        "currentWorkload",
        workload.toUpperCase()
    );


    setText(
        "drainRate",
        `${Number(data.historical_drain_rate || 0).toFixed(2)}% / hr`
    );


    const descriptions = {

        Coding:
            "VSCode activity detected. Your system is currently optimized for a coding workload.",

        Video:
            "Video activity detected. Display usage may increase battery consumption.",

        Whatsapp:
            "WhatsApp activity detected. Messaging activity is currently active.",

        Light:
            "Light system activity detected. No major workload is currently identified."
    };


    setText(
        "workloadDescription",
        descriptions[workload] ||
        "Current workload detected from system activity."
    );
}


function updateForecast(data) {

    const predicted =
        Number(data.ml_predicted_battery);


    if (!Number.isNaN(predicted)) {

        setText(
            "predictedBattery",
            `${predicted.toFixed(1)}%`
        );
    }
}


function updateApplications(applications) {

    const container =
        document.getElementById("applicationsList");


    if (!container) {
        return;
    }


    container.innerHTML = "";


    if (
        !Array.isArray(applications) ||
        applications.length === 0
    ) {

        container.innerHTML = `
            <div class="app-row">

                <div class="app-name">
                    <span class="app-number">--</span>
                    No active applications
                </div>

                <div class="app-track">
                    <div
                        class="app-fill"
                        style="width: 0%;"
                    ></div>
                </div>

                <strong>0%</strong>

            </div>
        `;

        return;
    }


    applications.forEach((app, index) => {

        const ram =
            Number(app.ram) || 0;


        const cpu =
            Number(app.cpu) || 0;


        const barWidth =
            Math.min(cpu * 1.8, 100);


        const row =
            document.createElement("div");


        row.className = "app-row";


        row.innerHTML = `

            <div class="app-name">

                <span class="app-number">
                    ${String(index + 1).padStart(2, "0")}
                </span>

                ${escapeHTML(app.name || "Unknown")}

            </div>


            <div class="app-track">

                <div
                    class="app-fill"
                    style="width: ${barWidth}%"
                ></div>

            </div>


            <strong>
                ${cpu.toFixed(1)}%
            </strong>
        `;


        row.title =
            `CPU: ${cpu.toFixed(1)}% | RAM: ${ram.toFixed(1)}%`;


        container.appendChild(row);
    });
}


function updateRecommendations(recommendations) {

    const container =
        document.getElementById("recommendationsList");


    if (!container) {
        return;
    }


    container.innerHTML = "";


    if (
        !Array.isArray(recommendations) ||
        recommendations.length === 0
    ) {

        container.innerHTML = `

            <button class="recommendation">

                <span class="rec-number">
                    ✓
                </span>

                <span class="rec-text">
                    No immediate optimization required
                </span>

                <span class="rec-arrow">
                    ✓
                </span>

            </button>

        `;

        return;
    }


    recommendations
        .slice(0, 3)
        .forEach((recommendation, index) => {

            const button =
                document.createElement("button");


            button.className =
                "recommendation";


            button.innerHTML = `

                <span class="rec-number">
                    ${String(index + 1).padStart(2, "0")}
                </span>

                <span class="rec-text">
                    ${escapeHTML(recommendation)}
                </span>

                <span class="rec-arrow">
                    →
                </span>

            `;


            container.appendChild(button);
        });
}


function escapeHTML(value) {

    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}


async function updateDashboard() {

    if (isFetching) {
        return;
    }


    isFetching = true;


    const controller =
        new AbortController();


    const timeout =
        setTimeout(
            () => controller.abort(),
            4000
        );


    try {

        const response =
            await fetch(
                API_URL,
                {
                    method: "GET",
                    cache: "no-store",
                    signal: controller.signal
                }
            );


        if (!response.ok) {

            throw new Error(
                `Backend returned HTTP ${response.status}`
            );
        }


        const data =
            await response.json();


        updateBattery(data);

        updateSystem(data);

        updateForecast(data);

        updateApplications(
            data.applications
        );

        updateRecommendations(
            data.recommendations
        );


        setText(
            "lastUpdated",
            `UPDATED ${new Date().toLocaleTimeString()}`
        );


        console.log(
            "LIVE SYSTEM DATA:",
            data
        );

    } catch (error) {

        console.error(
            "Dashboard update failed:",
            error.message
        );


        setText(
            "lastUpdated",
            "BACKEND OFFLINE"
        );

    } finally {

        clearTimeout(timeout);

        isFetching = false;
    }
}


/* START */

updateDashboard();


setInterval(
    updateDashboard,
    5000
);
