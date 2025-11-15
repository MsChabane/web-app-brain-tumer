function showTab(tab) {
	document
		.querySelectorAll(".tab-content")
		.forEach((t) => (t.style.display = "none"));
	document.getElementById(tab).style.display = "block";
}

function openDoctorModal() {
	document.getElementById("doctorModal").style.display = "flex";
}

function closeDoctorModal() {
	document.getElementById("doctorModal").style.display = "none";
}

function saveDoctor() {
	let name = document.getElementById("docName").value;
	let speciality = document.getElementById("docSpeciality").value;
	let exp = document.getElementById("docExperience").value;
	let phone = document.getElementById("docPhone").value;

	if (!name || !speciality || !exp || !phone) {
		alert("Please complete all fields!");
		return;
	}

	let row = `
            <tr>
                <td>${name}</td>
                <td>${speciality}</td>
                <td>${exp} years</td>
                <td>${phone}</td>
            </tr>
        `;

	document.getElementById("doctorTable").innerHTML += row;
	closeDoctorModal();
}

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

console.log("12");
