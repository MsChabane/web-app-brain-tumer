const personel_info = document.getElementById("personel_info");
function getRole() {
	const token = localStorage.getItem("token");
	const role = localStorage.getItem("role");

	if (!token || !role) {
		window.location.href = "/auth/login";
		return;
	}
	const page = window.location.pathname.split("/").pop();
	console.log(page);
	console.log(role);
	if (page !== role) {
		window.location.href = `/${role}`;
	}

	// if (role === "admin" && page !== "admin") window.location.href = "admin";
	// else if (role === "doctor" && page !== "doctor")
	// 	window.location.href = "/doctor";
	// else if (role === "patient" && page !== "patient")
	// 	window.location.href = "/patient";
	// else window.location.href = "/auth/login";
}

function logout() {
	localStorage.clear();
	window.location.href = "/login";
}

function back_to_login(message) {
	pushNotification(message, "error", 2000);
	setTimeout(() => {
		window.location.href = "/auth/login";
	}, 2000);
}

async function getPatientInfos() {
	const token = localStorage.getItem("token");
	if (!token) {
		back_to_login("Don't have access");
		return;
	}
	const res = await fetch("/patient/me", {
		method: "GET",
		headers: {
			"Content-Type": "application/json",
			Authorization: `Bearer ${token}`,
		},
	});
	const data = await res.json();
	if (res.ok) {
		personel_info.innerHTML += `<div class="info-item"><span>Name:</span> ${data.name}</div>`;
		personel_info.innerHTML += `<div class="info-item"><span>Surname:</span> ${data.surname}</div>`;
		personel_info.innerHTML += `<div class="info-item"><span>Age:</span> ${data.age}</div>`;
		personel_info.innerHTML += `<div class="info-item"><span>Gender:</span> ${
			data.gender == "M" ? "Male" : "Female"
		}</div>`;
		personel_info.innerHTML += `<div class="info-item"><span>Antecedents:</span> ${data.antecedents}</div>`;
		personel_info.innerHTML += `<div class="info-item"><span>Tumor status:</span> ${data.tumor_status}</div>`;
		personel_info.innerHTML += `<div class="info-item"><span>Final state:</span> ${data.final_state}</div>`;
		return;
	} else {
		back_to_login(data.detail);
	}
}

async function getallsymptons() {
	const token = localStorage.getItem("token");
	console.log(token);
	if (!token) {
		back_to_login("Don't have access");
		return;
	}
	const res = await fetch("/patient/get-all-symptoms", {
		method: "GET",
		headers: {
			"Content-Type": "application/json",
			Authorization: `Bearer ${token}`,
		},
	});
	const data = await res.json();
	console.log(data);
	if (res.ok) {
		console.log(data);

		fill_general_symotoms(data.general_symptoms);
		fill_specific_symptoms(data.specific_symtoms);
		fill_radio_images_table(data.radio_images);
		return;
	} else {
		back_to_login(data.detail);
	}
}

function fill_general_symotoms(gs) {
	const gs_table = document.getElementById("table-general-symtoms");
	gs_table.innerHTML = "";
	gs.forEach((e) => {
		gs_table.innerHTML += `<tr>
                     <td>${e.headaches}</td>
                    <td>${e.seizures}</td>
                    <td>${e.fatigue}</td>
                    <td>${e.drowsiness}</td>
                    <td>${e.memory_pb}</td>
                    <td>${e.memory_pb}</td>
                </tr>`;
	});
}
function fill_specific_symptoms(ss) {
	const ss_table = document.getElementById("table-specific-symptoms");
	ss_table.innerHTML = "";
	ss.forEach((e) => {
		ss_table.innerHTML += `<tr>
                    <td>${e.pressure}</td>
                    <td>${e.balance_loss} loss</td>
                    <td>${e.judgment_degradation}</td>
                    <td>${e.sense_degradation}</td>
                    <td>${e.lactation}</td>
                    <td>${e.swallowing}</td>
                    <td>${e.muscle}</td>
                </tr>`;
	});
}

function fill_radio_images_table(rd) {
	const rd_table = document.getElementById("table-radio-image");
	rd_table.innerHTML = "";
	rd.forEach((e) => {
		rd_table.innerHTML += `<tr>
                    <td>${e.type}</td>
                </tr>`;
	});
}

getRole();
getPatientInfos();
getallsymptons();
