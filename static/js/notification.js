function pushNotification(message, type = "info", duration = 3000) {
	const container = document.getElementById("notifications");
	const notif = document.createElement("div");
	notif.classList.add("notification");

	if (type === "success") notif.style.backgroundColor = "#27ae60";
	if (type === "error") notif.style.backgroundColor = "#c0392b";
	if (type === "warning") notif.style.backgroundColor = "#f39c12";

	notif.innerText = message;
	container.appendChild(notif);

	setTimeout(() => {
		notif.style.transition = "all 0.5s";
		notif.style.opacity = "0";
		notif.style.transform = "translateX(100%)";
		setTimeout(() => container.removeChild(notif), 500);
	}, duration);
}
