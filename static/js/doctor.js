function getRole() {
	const token = localStorage.getItem("token");
	const role = localStorage.getItem("role");

	if (!token || !role) {
		window.location.href = "/auth/login";
		return;
	}
	const page = window.location.pathname.split("/").pop();
<<<<<<< HEAD
=======

>>>>>>> f002710c5797fb5aff7828bc5c162eb279d7dbeb
	if (page !== role) {
		window.location.href = `/${role}`;
	}
}
getRole();

getRole()
const tabLinks = document.querySelectorAll(".tab-link");
const tabContents = document.querySelectorAll(".tab-content");
const patients_table = document.getElementById("patients-table");

tabLinks.forEach((link) => {
	link.addEventListener("click", (e) => {
		e.preventDefault();
		tabLinks.forEach((l) => l.classList.remove("active"));
		link.classList.add("active");
		const tabId = link.dataset.tab + "-tab";
		tabContents.forEach((tc) => (tc.style.display = "none"));
		document.getElementById(tabId).style.display = "block";
		if (tabId === "patients-tab") {
			patients_table.innerHTML = ``;
			fill_table_patients();
<<<<<<< HEAD
		}  else if (tabId === "profile-tab") {
=======
		} else if (tabId === "profile-tab") {
>>>>>>> f002710c5797fb5aff7828bc5c162eb279d7dbeb
			fill_user_info();
		}
	});
});

fill_table_patients();
function openModal(id) {
	document.getElementById(id).style.display = "flex";
}
function closeModal(id) {
	document.getElementById(id).style.display = "none";
}
fill_table_patients();

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
              <button class="btn-add" onclick="open_detail('${
								patient.id
							}')">View</button>
            </td>`;
	patients_table.appendChild(tr);
}

async function open_detail(id) {
	window.location.href = `/details/${id}`;
}

async function fill_table_patients() {
	await _call(
		"/doctor/get-patients",
		"GET",
		undefined,
		(data) => {
			data.forEach((element) => add_patient_to_table(element));
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
			document.getElementById("user-phone").innerHTML = data.phone_number;
			document.getElementById("user-role").innerHTML = data.role;
		},
		() => {}
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

function logout() {
	localStorage.clear();
	window.location.href = "/auth/login";
}
