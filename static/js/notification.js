const notification = document.getElementById("notification");
function showNotification(message, success = false, duration = 3000) {
	notification.textContent = message;
	notification.style.backgroundColor = success ? "#4BB543" : "#ff4d4d";
	notification.classList.add("show");
	setTimeout(() => notification.classList.remove("show"), duration);
}
