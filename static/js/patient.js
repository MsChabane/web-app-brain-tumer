const tabLinks = document.querySelectorAll(".tab-link");
const tabContents = document.querySelectorAll(".tab-content");
const patient_info_table = document.getElementById("patient-info");
const gs_info_table = document.getElementById("general-symptoms-info");
const ss_info_table = document.getElementById("specific-symptoms-info");
const rd_info_table = document.getElementById("radio-image-info");

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

function logout() {
	localStorage.clear();
	window.location.href = "/auth/login";
}
function openModal(id) {
	document.getElementById(id).style.display = "flex";
}
function closeModal(id) {
	document.getElementById(id).style.display = "none";
}

tabLinks.forEach((link) => {
	link.addEventListener("click", (e) => {
		e.preventDefault();
		tabLinks.forEach((l) => l.classList.remove("active"));
		link.classList.add("active");
		const tabId = link.dataset.tab + "-tab";
		tabContents.forEach((tc) => (tc.style.display = "none"));
		document.getElementById(tabId).style.display = "block";
		if (tabId === "info-tab") {
			fill_info();
		} else if (tabId === "profile-tab") {
			fill_user_info();
		}
	});
});
fill_info();

function fill_table_patient(patient) {
	patient_info_table.innerHTML = `
	<tr>
        <th>Name</th>
         <td>${patient.name}</td>
    </tr>
    <tr>
        <th>Surname</th>
        <td>${patient.surname}</td>
    </tr>
            <tr>
                <th>Age</th>
                <td>${patient.age}</td>
            </tr>
            <tr>
                <th>Gender</th>
                <td>${patient.gender == "M" ? "Male" : "Female"}</td>
            </tr>
            <tr>
                <th>Antecedents</th>
                <td>${patient.antecedents}</td>
            </tr>
            <tr>
                <th>Tumor Status</th>
                <td>${
									patient.tumor_status !== null
										? `<span class='badge badge-${
												patient.tumor_status == 0 ? "negative" : "positive"
										  }'>${
												patient.tumor_status == 0 ? "negative" : "positive"
										  }<span>`
										: "-"
								}</td>
            </tr>
            <tr>
                <th>Hospitalisation</th>
                <td>${
									patient.hospitalisation != null
										? patient.hospitalisation
										: "-"
								}</td>
            </tr>
            <tr>
                <th>Final State</th>
                <td>${
									patient.final_state != null ? patient.final_state : "-"
								}</td>
            </tr>
							${
								patient.doctor
									? `
		<tr>
                <th>Doctor</th>
                <td>${patient.doctor.name}</td>
        </tr>
		`
									: ""
							}
            
			`;
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

function fill_info() {
	_call(
		"/patient/me",
		"GET",
		undefined,
		(data) => {
			fill_table_patient(data);
		},
		() => {}
	);
	_call(
		"patient/get-latest-symptoms",
		"GET",
		undefined,
		(data) => {
			fill_table_general_symptoms(data.general_symptoms);
			fill_table_specific_symptoms(data.specific_symptoms);
			fill_table_radio_image(data.radio_image);
		},
		() => {}
	);
}

function fill_table_general_symptoms(general_symptoms) {
	if (general_symptoms) {
		gs_info_table.innerHTML = `
	<tr>
    	<th>Headaches</th>
        <td>${general_symptoms.headaches}</td>
    </tr>
    <tr>
        <th>Seizures</th>
         <td>${general_symptoms.seizures}</td>
    </tr>
    <tr>
        <th>Fatigue</th>
        <td>${general_symptoms.fatigue}</td>
    </tr>
    <tr>
        <th>Drowsiness</th>
       <td>${general_symptoms.drowsiness}</td>
    </tr>
    <tr>
        <th>Sleep Problems</th>
       <td>${general_symptoms.sleep_pb}</td>
    </tr>
    <tr>
        <th>Memory Problems</th>
       <td>${general_symptoms.memory_pb}</td>
    </tr> `;
	} else {
		gs_info_table.innerHTML = `<tr><th> No General Symptoms added. </th></tr > `;
	}
}

function fill_table_specific_symptoms(specific_symptoms) {
	if (specific_symptoms) {
		ss_info_table.innerHTML = `
	<tr>
    <th>Pressure</th>
        <td>${specific_symptoms.pressure}</td>
    </tr>
    <tr>
        <th>Balance Loss</th>
       <td>${specific_symptoms.balance_loss}</td>
    </tr>
    <tr>
        <th>Judgment Degradation</th>
       <td>${specific_symptoms.judgment_degradation}</td>
    </tr>
    <tr>
        <th>Sense Degradation</th>
        <td>${specific_symptoms.sense_degradation}</td>
    </tr>
    <tr>
        <th>Lactation</th>
      <td>${specific_symptoms.lactation}</td>
    </tr>
    <tr>
        <th>Swallowing</th>
     <td>${specific_symptoms.swallowing}</td>
    </tr>
    <tr>
        <th>Muscle Issues</th>
      <td>${specific_symptoms.muscle}</td>
    </tr>`;
	} else {
		ss_info_table.innerHTML = `<tr><th> No Specific Symptoms added. </th></tr > `;
	}
}
function fill_table_radio_image(rd_image) {
	if (rd_image) {
		rd_info_table.innerHTML = `
	<tr>
        <th>Type</th>
      <td>${rd_image.type}</td>
    </tr>
	`;
	} else {
		rd_info_table.innerHTML = `<tr><th> No Radio images added. </th></tr > `;
	}
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
