const form = document.getElementById("loginForm");
const submitBtn = document.getElementById("submitBtn");

form.addEventListener("submit", async (e) => {
	e.preventDefault();

	submitBtn.disabled = true;

	const phone = document.getElementById("phone").value.trim();
	const password = document.getElementById("password").value;

	if (!phone || !password) {
		pushNotification("Fill all fields", "warning");
		submitBtn.disabled = false;
		return;
	}

	try {
		const res = await fetch("/auth/login", {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({ phone_number: phone, password }),
		});

		const data = await res.json();

		if (res.ok) {
			localStorage.setItem("token", data.access_token);
			localStorage.setItem("role", data.role);
			const role = data.role;
			if (role === "admin") window.location.href = "/admin";
			else if (role === "doctor") window.location.href = "/doctor";
			else window.location.href = "/patient";

			return;
		} else {
			pushNotification(data.detail, "warning");
		}
		submitBtn.disabled = false;
	} catch (err) {
		pushNotification("Network error", "error");
		submitBtn.disabled = false;
	}
});
