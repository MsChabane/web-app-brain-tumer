function getRole() {
	const token = localStorage.getItem("token");
	const role = localStorage.getItem("role");

	if (!token || !role) {
		window.location.href = "/auth/login";
		return;
	}
	const page = window.location.pathname.split("/").pop();
	if (page !== role) {
		window.location.href = `/${role}`;
	}
}

getRole();

const tabLinks = document.querySelectorAll(".tab-link");
const tabContents = document.querySelectorAll(".tab-content");
const doctor_table = document.getElementById("doctors-table");
const patient_table = document.getElementById("patients-table");
const patient_no_asso_table = document.getElementById("patients-no-asso-table");
const user_table = document.getElementById("users-table");
const doctors_list_assoc = document.getElementById("doctors-list");

function getRole() {
	const token = localStorage.getItem("token");
	const role = localStorage.getItem("role");

	if (!token || !role) {
		window.location.href = "/auth/login";
		return;
	}
	const page = window.location.pathname.split("/").pop();

	if (page !== role) {
		window.location.href = `/${role}`;
	}
}
getRole();

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
		} else if (tabId === "associations-tab") {
			fill_table_patients_no_assoc();
			fill_list_doctors();
		}
		if (tabId === "profile-tab") {
			fill_user_info();
		}
	});
});

async function fill_dashboard() {
	await _call(
		"/dashboard/total",
		"GET",
		undefined,
		(data) => {
			console.log(data);
			document.getElementById("total-users").innerHTML = data.data.total_users;
			document.getElementById("total-patients").innerHTML =
				data.data.total_patients;
			document.getElementById("total-doctors").innerHTML =
				data.data.total_doctors;
		},
		() => {}
	);
}
fill_dashboard();

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
              <button class="btn-delete" onclick="openDeleteModal('Are you sure you want to delete this doctor?','${doctor.id}','doctor')">Delete</button>
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
            <td>${
							patient.tumor_status !== null
								? `<span class='badge badge-${
										patient.tumor_status == 0 ? "negative" : "positive"
								  }'>${
										patient.tumor_status == 0 ? "negative" : "positive"
								  }<span>`
								: "-"
						}</td>
            <td>${patient.hospitalisation || "-"}</td>
            <td>${patient.final_state || "-"}</td>
            <td>
              <button class="btn-update" onclick="update_patient_open_model('${
								patient.id
							}')">Update</button>
              <button class="btn-delete" onclick="openDeleteModal('Are you sure you want to delete this patient?','${
								patient.id
							}','patient')">Delete</button>
            </td>`;
	patient_table.appendChild(tr);
}

function add_doctor_to_list(doctor) {
	doctors_list_assoc.innerHTML += `
        <option value="${doctor.id}">${doctor.name}</option>
	`;
}

function open_associate_modal(id) {
	document.getElementById("patient-to-associate").value = id;
	openModal("associate-modal");
}

function add_patient_no_asso_to_table(patient) {
	const tr = document.createElement("tr");
	tr.dataset.patientId = patient.id;
	tr.innerHTML = `<td>${patient.name + " " + patient.surname} </td>
	<td>${patient.gender == "M" ? "Male" : "Female"}</td>
	<td>${patient.age}</td>
            <td>${patient.antecedents}</td>
            <td>${
							patient.tumor_status !== null
								? `<span class='badge badge-${
										patient.tumor_status == 0 ? "negative" : "positive"
								  }'>${
										patient.tumor_status == 0 ? "negative" : "positive"
								  }<span>`
								: "-"
						}</td>
            <td>${patient.hospitalisation || "-"}</td>
            <td>${patient.final_state || "-"}</td>
			<td>${patient.doctor ? patient.doctor.name : "-"}</td>
            <td>
              <button class="btn-add" onclick="open_associate_modal('${
								patient.id
							}')">associate</button>
            </td>`;
	patient_no_asso_table.appendChild(tr);
}
async function fill_list_doctors() {
	doctors_list_assoc.innerHTML = `<option value="">Select doctor</option>`;
	await _call(
		"/doctor/all?page=1&limit=1000",
		"GET",
		undefined,
		(data) => {
			data.forEach((element) => add_doctor_to_list(element));
		},
		() => {}
	);
}

async function associate() {
	const doctor = doctors_list_assoc.value;
	const patient_id = document.getElementById("patient-to-associate").value;
	if (!doctor) {
		showNotification("Please select a doctor!");
	}
	const btn = document.getElementById("submit-associate-btn");
	const text = document.getElementById("associate-submit-text");
	const spinner = document.getElementById("associate-submit-spinner");

	btn.disabled = true;
	text.style.display = "none";
	spinner.style.display = "inline-block";
	await _call(
		`/patient/${patient_id}/associate-to/${doctor}`,
		"POST",
		undefined,
		(data) => {
			console.log(data);
			showNotification("Patient is assciated!", true);
			btn.disabled = false;
			text.style.display = "inline";
			spinner.style.display = "none";
			document
				.querySelector(`[data-patient-id='${patient_id}']`)
				.children.item(7).innerHTML = data.doctor.name;
			closeModal("associate-modal");
		},
		() => {
			btn.disabled = false;
			text.style.display = "inline";
			spinner.style.display = "none";
		}
	);
}

function add_user_to_table(user) {
	const tr = document.createElement("tr");
	tr.id = user.id;
	tr.innerHTML = `<td>${user.phone_number}</td>
            <td>
							
				 <span class='badge badge-${
						user.role == "admin"
							? "positive"
							: user.role === "doctor"
							? "negative"
							: "null"
					}'>${user.role}<span>
								
						</td>
		${
			user.role === "admin"
				? `<td><button class="btn-delete" onclick="openDeleteModal('Are you sure you want to delete this admin?','${user.id}','admin')">Delete</button></td>	`
				: "-"
		}
					`;
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
	patient_table.innerHTML = "";
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

async function fill_table_patients_no_assoc() {
	patient_no_asso_table.innerHTML = "";
	await _call(
		"/patient/all",
		"GET",
		undefined,
		(data) => {
			data.forEach((element) => add_patient_no_asso_to_table(element));
		},
		() => {}
	);
}

async function fill_user_info() {
	await _call(
		"/auth/profile",
		"GET",
		undefined,
		(data) => {
			console.log(data);
			document.getElementById("user-phone").innerHTML = data.phone_number;
			document.getElementById("user-role").innerHTML = data.role;
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

async function change_password() {
	const new_password = document.getElementById("new-password").value.trim();
	const confirm_password = document
		.getElementById("confirm-password")
		.value.trim();
	if (!new_password || !confirm_password) {
		showNotification("Please fill all fields!");
		return;
	}
	if (new_password !== confirm_password) {
		showNotification("Passords miss match!");
		return;
	}

	const btn = document.getElementById("submit-changepwd-btn");
	const text = document.getElementById("changepwd-submit-text");
	const spinner = document.getElementById("changepwd-submit-spinner");

	btn.disabled = true;
	text.style.display = "none";
	spinner.style.display = "inline-block";

	await _call(
		"/auth/user/change-password",
		"POST",
		{
			password: new_password,
		},
		(data) => {
			showNotification("Password Changed !", true);
			btn.disabled = false;
			text.style.display = "inline";
			spinner.style.display = "none";
			closeModal("change-password-modal");
			document.getElementById("new-password").value = "";
			document.getElementById("confirm-password").value;
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

async function delete_(role, id) {
	const btn = document.getElementById("submit-admin-btn");
	const text = document.getElementById("delete-text");
	const spinner = document.getElementById("delete-spinner");

	btn.disabled = true;
	text.style.display = "none";
	spinner.style.display = "inline-block";

	await _call(
		role === "admin" ? `/auth/users/admin/${id}` : `/${role}/${id}`,
		"DELETE",
		undefined,
		(data) => {
			console.log(data);
			document.getElementById(id).remove();
			closeDeleteModal();
			btn.disabled = false;
			text.style.display = "inline";
			spinner.style.display = "none";
			document.getElementById("delete-id").value = "";
		},
		() => {
			btn.disabled = false;
			text.style.display = "inline";
			spinner.style.display = "none";
		}
	);
}

function openDeleteModal(message, id, type) {
	document.getElementById("delete-message").innerText = message;
	document.getElementById("delete-id").value = id;
	document.getElementById("confirm-delete-btn").onclick = () => {
		delete_(type, id);
	};
	document.getElementById("delete-confirm-modal").style.display = "flex";
}

function closeDeleteModal() {
	document.getElementById("delete-confirm-modal").style.display = "none";
}

function logout() {
	localStorage.clear();
	window.location.href = "/auth/login";
}
