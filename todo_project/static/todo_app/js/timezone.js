document.addEventListener("DOMContentLoaded", () => {
    const completedTimes = document.querySelectorAll(".completed-time");

    completedTimes.forEach(timeElement => {
        const utcTimestamp = timeElement.getAttribute("data-timestamp");

        if (utcTimestamp) {
            const localDate = new Date(utcTimestamp); // Convert UTC to local
            const formattedTime = localDate.toLocaleString(undefined, {
                year: "numeric",
                month: "short",
                day: "numeric",
                hour: "2-digit",
                minute: "2-digit",
            });

            timeElement.textContent = `(Completed: ${formattedTime})`; // Replace text
        }
    });
});
