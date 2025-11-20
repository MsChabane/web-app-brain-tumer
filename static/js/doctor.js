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

const tabLinks = document.querySelectorAll(".tab-link");
const tabContents = document.querySelectorAll(".tab-content");
const check_table = document.getElementById("checks-table");
const patient_tabke = document.getElementById("patients-table");


tabLinks.forEach((link) => {
	link.addEventListener("click", (e) => {
		e.preventDefault();
		tabLinks.forEach((l) => l.classList.remove("active"));
		link.classList.add("active");
		const tabId = link.dataset.tab + "-tab";
		tabContents.forEach((tc) => (tc.style.display = "none"));
		document.getElementById(tabId).style.display = "block";
		if (tabId === "doctors-tab") {
			fill_table_doctors();
		} else if (tabId === "patients-tab") {
			fill_table_patients();
		} else if (tabId === "users-tab") {
			fill_table_users();
		} else if (tabId === "dashboard-tab") {
			fill_dashboard();
		}
	});
});

function openModal(id) {
	document.getElementById(id).style.display = "flex";
}
function closeModal(id) {
	document.getElementById(id).style.display = "none";
}

function add_patient_to_table(patient) {
	const tr = document.createElement("tr");
	tr.id = patient.id;
	tr.innerHTML = `<td>${patient.name + " " + patient.surname} </td>
	<td>${patient.gender == "M" ? "Male" : "Female"}</td>
	<td>${patient.age}</td>
            <td>${patient.antecedents}</td>
            <td>${patient.tumor_status || "-"}</td>
            <td>${patient.hospitalisation || "-"}</td>
            <td>${patient.final_state || "-"}</td>
            <td>
              <button class="btn-add" onclick="openModal('add-gs-modal')">Add GS</button>
              <button class="btn-add" onclick="openModal('add-ss-modal')">Add SS</button>
              <button class="btn-add" onclick="openModal('add-rd-modal')">Add RI</button>
            </td>`;
	patient_tabke.appendChild(tr);

}

add_patient_to_table({
    
})



