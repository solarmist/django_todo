document.addEventListener("DOMContentLoaded", () => {
    const toasts = document.querySelectorAll(".toast");
    toasts.forEach((toast) => {
        setTimeout(() => {
            toast.classList.add("fade-in-out");
        }, 3000);  // Wait 3 seconds before fading out
    });
});
