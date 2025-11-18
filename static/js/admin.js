const tabLinks = document.querySelectorAll(".tab-link");
const tabContents = document.querySelectorAll(".tab-content");
const doctor_table = document.getElementById("doctors-table");
const patient_tabke = document.getElementById("patients-table");
const user_table = document.getElementById("users-table");

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
		} else if (tabId == "users-tab") {
			fill_table_users();
		}
	});
});

// Modals
function openModal(id) {
	document.getElementById(id).style.display = "flex";
}
function closeModal(id) {
	document.getElementById(id).style.display = "none";
}

function add_doctor_to_table(doctor) {
	const tr = document.createElement("tr");
	tr.id = doctor.id;
	tr.innerHTML = `<td>${doctor.name}</td>
            <td>${doctor.specialty}</td>
            <td>${doctor.years_experience}</td>
            <td>
              <button class="btn-update" onclick="update_doctor_open_model('${doctor.id}')">Update</button>
              <button class="btn-delete" onclick="showNotification('Delete Doctor clicked!')">Delete</button>
            </td>`;
	doctor_table.appendChild(tr);
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
              <button class="btn-update" onclick="update_patient_open_model('${
								patient.id
							}')">Update</button>
              <button class="btn-delete" onclick="showNotification('Delete Patient clicked!')">Delete</button>
            </td>`;
	patient_tabke.appendChild(tr);
}
function add_user_to_table(user) {
	const tr = document.createElement("tr");
	tr.id = user.id;
	tr.innerHTML = `<td>${user.phone_number}</td>
            <td>${user.role}</td>`;
	user_table.appendChild(tr);
}

async function fill_table_users() {
	user_table.innerHTML = "";
	await _call(
		"/auth/users/all",
		"GET",
		undefined,
		(data) => {
			data.forEach((element) => add_user_to_table(element));
		},
		() => {}
	);
}
async function fill_table_doctors() {
	doctor_table.innerHTML = "";
	await _call(
		"/doctor/all",
		"GET",
		undefined,
		(data) => {
			data.forEach((element) => add_doctor_to_table(element));
		},
		() => {}
	);
}
async function fill_table_patients() {
	patient_tabke.innerHTML = "";
	await _call(
		"/patient/all",
		"GET",
		undefined,
		(data) => {
			data.forEach((element) => add_patient_to_table(element));
		},
		() => {}
	);
}

async function submitPatient() {
	const name = document.getElementById("patient-name").value;
	const surname = document.getElementById("patient-surname").value;
	const age = document.getElementById("patient-age").value;
	const gender = document.getElementById("patient-gender").value;
	const antecedents = document.getElementById("patient-antecedents").value;
	const phone = document.getElementById("patient-phone").value;

	if (!name || !surname || !age || !gender || !antecedents || !phone) {
		showNotification("Please fill all fields!");
		return;
	}

	const btn = document.getElementById("submit-patient-btn");
	const text = document.getElementById("patient-submit-text");
	const spinner = document.getElementById("patient-submit-spinner");

	btn.disabled = true;
	text.style.display = "none";
	spinner.style.display = "inline-block";
	await _call(
		"/patient/new-patient",
		"POST",
		{
			patient: {
				name: name,
				surname: surname,
				age: age,
				gender: gender,
				antecedents: antecedents,
			},
			user: { phone_number: phone, password: phone },
		},
		(data) => {
			showNotification("Patient created successfully!", true);
			btn.disabled = false;
			text.style.display = "inline";
			spinner.style.display = "none";
			add_patient_to_table(data);
			document.getElementById("patient-name").value = "";
			document.getElementById("patient-surname").value = "";
			document.getElementById("patient-age").value = "";
			document.getElementById("patient-gender").value = "";
			document.getElementById("patient-antecedents").value = "";
			document.getElementById("patient-phone").value = "";
			closeModal("add-patient-modal");
		},
		() => {
			btn.disabled = false;
			text.style.display = "inline";
			spinner.style.display = "none";
		}
	);
}
async function submitDoctor() {
	const name = document.getElementById("doctor-name").value.trim();
	const spc = document.getElementById("doctor-speciality").value;
	const exp = document.getElementById("doctor-year-of-exp").value;
	const phone = document.getElementById("doctor-phone").value.trim();

	if (!name || !spc || !exp || !phone) {
		showNotification("Please fill all fields!");
		return;
	}

	const btn = document.getElementById("submit-doctor-btn");
	const text = document.getElementById("doctor-submit-text");
	const spinner = document.getElementById("doctor-submit-spinner");

	btn.disabled = true;
	text.style.display = "none";
	spinner.style.display = "inline-block";

	await _call(
		"/doctor/new-doctor",
		"POST",
		{
			doctor: {
				name: name,
				specialty: spc,
				years_experience: exp,
			},
			user: {
				phone_number: phone,
				password: phone,
			},
		},
		(data) => {
			showNotification("Doctor created successfully!", true);
			add_doctor_to_table(data);
			console.log(data);
			btn.disabled = false;
			text.style.display = "inline";
			spinner.style.display = "none";
			closeModal("add-doctor-modal");
			document.getElementById("doctor-name").value = "";
			document.getElementById("doctor-speciality").value = "";
			document.getElementById("doctor-year-of-exp").value = "";
			document.getElementById("doctor-phone").value = "";
		},
		() => {
			btn.disabled = false;
			text.style.display = "inline";
			spinner.style.display = "none";
		}
	);
}

async function submitAdmin() {
	const phone = document.getElementById("admin-phone").value.trim();

	if (!phone) {
		showNotification("Please fill all fields!");
		return;
	}
	const btn = document.getElementById("submit-admin-btn");
	const text = document.getElementById("admin-submit-text");
	const spinner = document.getElementById("admin-submit-spinner");

	btn.disabled = true;
	text.style.display = "none";
	spinner.style.display = "inline-block";

	await _call(
		"/auth/create-admin",
		"POST",
		{
			phone_number: phone,
		},
		(data) => {
			showNotification("Admin created successfully!", true);
			add_user_to_table(data);
			btn.disabled = false;
			text.style.display = "inline";
			spinner.style.display = "none";
			closeModal("add-admin-modal");
			document.getElementById("admin-phone").value = "";
		},
		() => {
			btn.disabled = false;
			text.style.display = "inline";
			spinner.style.display = "none";
		}
	);
}

async function _call(uri, method, body = undefined, success, failed) {
	const token = localStorage.getItem("token");
	try {
		const res = await fetch(uri, {
			method: method,
			body: body ? JSON.stringify(body) : body,
			headers: {
				"Content-Type": "application/json",
				Authorization: `Bearer ${token}`,
			},
		});
		const data = await res.json();
		if (res.ok) {
			success(data);
		} else {
			if (res.status === 401) {
				showNotification("session expire ! log in again...");
				localStorage.removeItem("token");
				localStorage.removeItem("role");
				setTimeout(() => (window.location.href = "/auth/login"), 3000);
			} else {
				showNotification(data.detail);
				failed();
			}
		}
	} catch (err) {
		showNotification("Network error");
		console.log(err);
	}
}

function update_doctor_open_model(id) {
	const selected_row = document.getElementById(id);
	document.getElementById("doctor-name-update").value =
		selected_row.children.item(0).innerHTML;
	document.getElementById("doctor-speciality-update").value =
		selected_row.children.item(1).innerHTML;
	document.getElementById("doctor-year-of-exp-update").value =
		selected_row.children.item(2).innerHTML;
	document.getElementById("doctor-id").value = id;
	openModal("update-doctor-modal");
}

function update_patient_open_model(id) {
	const selected_row = document.getElementById(id);
	const [name, surname] = selected_row.children.item(0).innerHTML.split(" ");
	document.getElementById("update-patient-name").value = name;

	document.getElementById("update-patient-surname").value = surname;

	document.getElementById("update-patient-gender").value = selected_row.children
		.item(1)
		.innerHTML.at(0);
	document.getElementById("update-patient-age").value = parseInt(
		selected_row.children.item(2).innerHTML
	);

	document.getElementById("update-patient-antecedents").value =
		selected_row.children.item(3).innerHTML;
	document.getElementById("patient-id").value = id;
	openModal("update-patient-modal");
}

async function update_doctor() {
	const name = document.getElementById("doctor-name-update").value.trim();
	const spc = document.getElementById("doctor-speciality-update").value.trim();
	const exp = document.getElementById("doctor-year-of-exp-update").value;
	if (!name || !spc || !exp) {
		showNotification("Please fill all fields!");
		return;
	}
	const id = document.getElementById("doctor-id").value;
	const btn = document.getElementById("submit-doctor-btn-update");
	const text = document.getElementById("doctor-submit-text-update");
	const spinner = document.getElementById("doctor-submit-spinner-update");

	btn.disabled = true;
	text.style.display = "none";
	spinner.style.display = "inline-block";
	await _call(
		`/doctor/${id}`,
		"PUT",
		{
			name: name,
			specialty: spc,
			years_experience: exp,
		},
		(data) => {
			showNotification("Doctor Updated Successfely", true);
			btn.disabled = false;
			text.style.display = "inline";
			spinner.style.display = "none";
			const selected_row = document.getElementById(data.id);
			selected_row.children.item(0).innerHTML = name;
			selected_row.children.item(1).innerHTML = spc;
			selected_row.children.item(2).innerHTML = exp;
			document.getElementById("doctor-id").value = "";
			closeModal("update-doctor-modal");
		},
		() => {
			btn.disabled = false;
			text.style.display = "inline";
			spinner.style.display = "none";
		}
	);
}
async function update_patient() {
	const name = document.getElementById("update-patient-name").value.trim();
	const surname = document
		.getElementById("update-patient-surname")
		.value.trim();
	const gender = document.getElementById("update-patient-gender").value;
	const age = document.getElementById("update-patient-age").value;
	const antecedents = document.getElementById(
		"update-patient-antecedents"
	).value;

	if (!name || !surname || !gender || !age || !antecedents) {
		showNotification("Please fill all fields!");
		return;
	}

	const id = document.getElementById("patient-id").value;
	const btn = document.getElementById("submit-patient-btn-update");
	const text = document.getElementById("patient-submit-text-update");
	const spinner = document.getElementById("patient-submit-spinner-update");

	btn.disabled = true;
	text.style.display = "none";
	spinner.style.display = "inline-block";
	await _call(
		`/patient/${id}`,
		"PUT",
		{
			name: name,
			surname,
			age,
			antecedents,
			gender,
		},
		(data) => {
			showNotification("Patient Updated Successfely", true);
			btn.disabled = false;
			text.style.display = "inline";
			spinner.style.display = "none";
			const selected_row = document.getElementById(data.id);
			selected_row.children.item(0).innerHTML = name + " " + surname;
			selected_row.children.item(1).innerHTML =
				gender == "M" ? "Male" : "Female";
			selected_row.children.item(2).innerHTML = age;
			selected_row.children.item(3).innerHTML = antecedents;
			document.getElementById("patient-id").value = "";
			closeModal("update-patient-modal");
		},
		() => {
			btn.disabled = false;
			text.style.display = "inline";
			spinner.style.display = "none";
		}
	);
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
