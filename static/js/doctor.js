function getRole() {
	const token = localStorage.getItem("token");
	const role = localStorage.getItem("role");

	if (!token || !role) {
		window.location.href = "/auth/login";
		return;
	}
	const page = window.location.pathname.split("/").pop();
	console.log(role);
	console.log(page);
	if (page !== role) {
		window.location.href = `/${role}`;
	}
}
