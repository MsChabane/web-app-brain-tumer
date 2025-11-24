const patient_info_table = document.getElementById("patient-info");
const gs_table = document.getElementById("gs-table");
const ss_table = document.getElementById("ss-table");
const rd_table = document.getElementById("rd-table");
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

const id = window.location.href.split("/").pop();
fill_info();
fill_tables_symptoms();
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

function fill_info() {
	_call(
		"/patient/" + id,
		"GET",
		undefined,
		(data) => {
			fill_table_patient(data);
		},
		() => {}
	);
}

function add_general_symptoms_to_table(gs, inTheTop = false) {
	const tr = document.createElement("tr");
	tr.id = gs.id;
	tr.innerHTML = `
	<td>${gs.headaches}</td>
    <td>${gs.seizures}</td>
    <td>${gs.fatigue}</td>
    <td>${gs.drowsiness}</td>
    <td>${gs.sleep_pb}</td>
    <td>${gs.memory_pb}</td>
    <td>${gs.created_at.split("T")[0]}</td>
	<td>
	<button class='btn-update' onclick="openUpdateGSModal('${
		gs.id
	}')">update</button>
	
	</td>
	`;
	if (inTheTop) {
		gs_table.prepend(tr);
	} else {
		gs_table.appendChild(tr);
	}
}
function add_specific_symptoms_to_table(ss, inTheTop = false) {
	const tr = document.createElement("tr");
	tr.id = ss.id;
	tr.innerHTML = `
	<td>${ss.pressure}</td>
    <td>${ss.balance_loss}</td>
    <td>${ss.judgment_degradation}</td>
    <td>${ss.sense_degradation}</td>
    <td>${ss.lactation}</td>
    <td>${ss.swallowing}</td>
    <td>${ss.muscle}</td>
    <td>${ss.created_at.split("T")[0]}</td>
	<td>
	<button class='btn-update'onclick="openUpdateSSModal('${
		ss.id
	}')" >update</button>
	
	</td>
	`;
	if (inTheTop) {
		ss_table.prepend(tr);
	} else {
		ss_table.appendChild(tr);
	}
}
function add_radio_image_to_table(rd, inTheTop = false) {
	const tr = document.createElement("tr");
	tr.id = rd.id;
	tr.innerHTML = `
	<td>${rd.type}</td>
    <td>${rd.created_at.split("T")[0]}</td>
	<td>
	<button class='btn-update' onclick="openUpdateRDModal('${
		rd.id
	}')">update</button>
	
	</td>
	`;
	if (inTheTop) {
		rd_table.prepend(tr);
	} else {
		rd_table.appendChild(tr);
	}
}

function fill_gs_table(general_symptms) {
	gs_table.innerHTML = ``;

	general_symptms.forEach((gs) => {
		add_general_symptoms_to_table(gs);
	});
}

function fill_ss_table(specific_symptoms) {
	ss_table.innerHTML = ``;

	specific_symptoms.forEach((ss) => {
		add_specific_symptoms_to_table(ss);
	});
}
function fill_rd_table(radio_image) {
	rd_table.innerHTML = ``;
	radio_image.forEach((rd) => {
		add_radio_image_to_table(rd);
	});
}

async function fill_tables_symptoms() {
	await _call(
		`/patient/${id}/get-all-symptoms`,
		"GET",
		undefined,
		(data) => {
			console.log(data);
			fill_gs_table(data.general_symptoms);
			fill_ss_table(data.specific_symtoms);
			fill_rd_table(data.radio_images);
		},
		() => {}
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

function openModal(id) {
	document.getElementById(id).style.display = "flex";
}
function closeModal(id) {
	document.getElementById(id).style.display = "none";
}

async function add_general_symtoms() {
	const headaches = document.getElementById("gs-headaches-add").value;
	const seizures = document.getElementById("gs-seizures-add").value;
	const fatigue = document.getElementById("gs-fatigue-add").value;
	const drowsiness = document.getElementById("gs-drowsiness-add").value;
	const sleep_pb = document.getElementById("gs-sleep_pb-add").value;
	const memory_pb = document.getElementById("gs-memory_pb-add").value;
	if (
		!headaches ||
		!seizures ||
		!fatigue ||
		!drowsiness ||
		!sleep_pb ||
		!memory_pb
	) {
		showNotification("Please fill all fields!");
		return;
	}
	const btn = document.getElementById("submit-gs-btn");
	const text = document.getElementById("gs-submit-text");
	const spinner = document.getElementById("gs-submit-spinner");

	btn.disabled = true;
	text.style.display = "none";
	spinner.style.display = "inline-block";
	await _call(
		`/patient/${id}/add-general-symptoms`,
		"POST",
		{
			headaches,
			seizures,
			sleep_pb,
			memory_pb,
			fatigue,
			drowsiness,
		},
		(data) => {
			console.log(data);
			showNotification("General Symtoms is added Successfelly!", true);
			add_general_symptoms_to_table(data, true);
			btn.disabled = false;
			text.style.display = "inline";
			spinner.style.display = "none";
			closeModal("add-gs-modal");
			document.getElementById("gs-headaches-add").value = "";
			document.getElementById("gs-seizures-add").value = "";
			document.getElementById("gs-fatigue-add").value = "";
			document.getElementById("gs-drowsiness-add").value = "";
			document.getElementById("gs-sleep_pb-add").value = "";
			document.getElementById("gs-memory_pb-add").value = "";
		},
		() => {
			btn.disabled = false;
			text.style.display = "inline";
			spinner.style.display = "none";
		}
	);
}

async function add_specific_symtoms() {
	const pressure = document.getElementById("ss-pressure-add").value;
	const balance_loss = document.getElementById("ss-balance_loss-add").value;
	const judgment_degradation = document.getElementById(
		"ss-judgment_degradation-add"
	).value;
	const sense_degradation = document.getElementById(
		"ss-sense_degradation-add"
	).value;
	const lactation = document.getElementById("ss-lactation-add").value;
	const swallowing = document.getElementById("ss-swallowing-add").value;
	const muscle = document.getElementById("ss-muscle-add").value;

	if (
		!pressure ||
		!balance_loss ||
		!judgment_degradation ||
		!sense_degradation ||
		!swallowing ||
		!lactation ||
		!muscle
	) {
		showNotification("Please fill all fields!");
		return;
	}
	const btn = document.getElementById("submit-ss-btn");
	const text = document.getElementById("ss-submit-text");
	const spinner = document.getElementById("ss-submit-spinner");

	btn.disabled = true;
	text.style.display = "none";
	spinner.style.display = "inline-block";
	await _call(
		`/patient/${id}/add-specific-symptoms`,
		"POST",
		{
			pressure,
			balance_loss,
			judgment_degradation,
			sense_degradation,
			swallowing,
			muscle,
			lactation,
		},
		(data) => {
			console.log(data);
			showNotification("Specific Symtoms is added Successfelly!", true);
			add_specific_symptoms_to_table(data, true);
			btn.disabled = false;
			text.style.display = "inline";
			spinner.style.display = "none";
			closeModal("add-ss-modal");
			document.getElementById("ss-pressure-add").value = "";
			document.getElementById("ss-balance_loss-add").value = "";
			document.getElementById("ss-judgment_degradation-add").value = "";
			document.getElementById("ss-sense_degradation-add").value = "";
			document.getElementById("ss-lactation-add").value = "";
			document.getElementById("ss-swallowing-add").value = "";
			document.getElementById("ss-muscle-add").value = "";
		},
		() => {
			btn.disabled = false;
			text.style.display = "inline";
			spinner.style.display = "none";
		}
	);
}

async function add_radio_image_symtoms() {
	const type = document.getElementById("rd-type-add").value;

	if (!type) {
		showNotification("Please fill all fields!");
		return;
	}
	const btn = document.getElementById("submit-rd-btn");
	const text = document.getElementById("rd-submit-text");
	const spinner = document.getElementById("rd-submit-spinner");

	btn.disabled = true;
	text.style.display = "none";
	spinner.style.display = "inline-block";
	await _call(
		`/patient/${id}/add-radioimage-symptoms`,
		"POST",
		{
			type,
		},
		(data) => {
			showNotification("Radio Image Type is added Successfelly!", true);
			add_radio_image_to_table(data, true);
			btn.disabled = false;
			text.style.display = "inline";
			spinner.style.display = "none";
			closeModal("add-rd-modal");
			document.getElementById("rd-type-add").value = "";
		},
		() => {
			btn.disabled = false;
			text.style.display = "inline";
			spinner.style.display = "none";
		}
	);
}

function openUpdateGSModal(gs_id) {
	const selected_row = document.getElementById(gs_id);

	document.getElementById("gs-headaches-update").value =
		selected_row.children.item(0).innerHTML;
	document.getElementById("gs-seizures-update").value =
		selected_row.children.item(1).innerHTML;
	document.getElementById("gs-fatigue-update").value =
		selected_row.children.item(2).innerHTML;
	document.getElementById("gs-drowsiness-update").value =
		selected_row.children.item(3).innerHTML;
	document.getElementById("gs-sleep_pb-update").value =
		selected_row.children.item(4).innerHTML;
	document.getElementById("gs-memory_pb-update").value =
		selected_row.children.item(5).innerHTML;
	document.getElementById("gs-id").value = gs_id;
	openModal("update-gs-modal");
}

async function update_general_symtoms() {
	const headaches = document.getElementById("gs-headaches-update").value;
	const seizures = document.getElementById("gs-seizures-update").value;
	const fatigue = document.getElementById("gs-fatigue-update").value;
	const drowsiness = document.getElementById("gs-drowsiness-update").value;
	const sleep_pb = document.getElementById("gs-sleep_pb-update").value;
	const memory_pb = document.getElementById("gs-memory_pb-update").value;
	if (
		!headaches ||
		!seizures ||
		!fatigue ||
		!drowsiness ||
		!sleep_pb ||
		!memory_pb
	) {
		showNotification("Please fill all fields!");
		return;
	}
	const gs_id = document.getElementById("gs-id").value;
	const btn = document.getElementById("submit-gs-btn-update");
	const text = document.getElementById("gs-submit-text-update");
	const spinner = document.getElementById("gs-submit-spinner-update");

	btn.disabled = true;
	text.style.display = "none";
	spinner.style.display = "inline-block";
	await _call(
		`/patient/general-symptoms/${gs_id}`,
		"PUT",
		{
			headaches,
			seizures,
			sleep_pb,
			memory_pb,
			fatigue,
			drowsiness,
		},
		(data) => {
			showNotification("General Symtoms is updated!", true);
			btn.disabled = false;
			text.style.display = "inline";
			spinner.style.display = "none";
			const selected_row = document.getElementById(gs_id);
			selected_row.children.item(0).innerHTML = headaches;
			selected_row.children.item(1).innerHTML = seizures;
			selected_row.children.item(2).innerHTML = fatigue;
			selected_row.children.item(3).innerHTML = drowsiness;
			selected_row.children.item(4).innerHTML = sleep_pb;
			selected_row.children.item(5).innerHTML = memory_pb;
			document.getElementById("gs-id").value = "";
			closeModal("update-gs-modal");
		},
		() => {
			btn.disabled = false;
			text.style.display = "inline";
			spinner.style.display = "none";
		}
	);
}

function openUpdateSSModal(ss_id) {
	const selected_row = document.getElementById(ss_id);

	document.getElementById("ss-pressure-update").value =
		selected_row.children.item(0).innerHTML;
	document.getElementById("ss-balance_loss-update").value =
		selected_row.children.item(1).innerHTML;
	document.getElementById("ss-judgment_degradation-update").value =
		selected_row.children.item(2).innerHTML;
	document.getElementById("ss-sense_degradation-update").value =
		selected_row.children.item(3).innerHTML;
	document.getElementById("ss-lactation-update").value =
		selected_row.children.item(4).innerHTML;
	document.getElementById("ss-swallowing-update").value =
		selected_row.children.item(5).innerHTML;
	document.getElementById("ss-muscle-update").value =
		selected_row.children.item(6).innerHTML;
	document.getElementById("ss-id").value = ss_id;
	openModal("update-ss-modal");
}

async function update_specific_symtoms() {
	const pressure = document.getElementById("ss-pressure-update").value;
	const balance_loss = document.getElementById("ss-balance_loss-update").value;
	const judgment_degradation = document.getElementById(
		"ss-judgment_degradation-update"
	).value;
	const sense_degradation = document.getElementById(
		"ss-sense_degradation-update"
	).value;
	const lactation = document.getElementById("ss-lactation-update").value;
	const swallowing = document.getElementById("ss-swallowing-update").value;
	const muscle = document.getElementById("ss-muscle-update").value;

	if (
		!pressure ||
		!balance_loss ||
		!judgment_degradation ||
		!sense_degradation ||
		!swallowing ||
		!lactation ||
		!muscle
	) {
		showNotification("Please fill all fields!");
		return;
	}
	const ss_id = document.getElementById("ss-id").value;
	const btn = document.getElementById("submit-ss-btn-update");
	const text = document.getElementById("ss-submit-text-update");
	const spinner = document.getElementById("ss-submit-spinner-update");

	btn.disabled = true;
	text.style.display = "none";
	spinner.style.display = "inline-block";
	await _call(
		`/patient/specific-symptoms/${ss_id}`,
		"PUT",
		{
			pressure,
			balance_loss,
			judgment_degradation,
			sense_degradation,
			swallowing,
			muscle,
			lactation,
		},
		(data) => {
			showNotification("Specific Symtoms is added Successfelly!", true);

			btn.disabled = false;
			text.style.display = "inline";
			spinner.style.display = "none";
			const selected_row = document.getElementById(ss_id);
			selected_row.children.item(0).innerHTML = pressure;
			selected_row.children.item(1).innerHTML = balance_loss;
			selected_row.children.item(2).innerHTML = judgment_degradation;
			selected_row.children.item(3).innerHTML = sense_degradation;
			selected_row.children.item(4).innerHTML = lactation;
			selected_row.children.item(5).innerHTML = swallowing;
			selected_row.children.item(6).innerHTML = muscle;
			document.getElementById("ss-id").value = "";
			closeModal("update-ss-modal");
		},
		() => {
			btn.disabled = false;
			text.style.display = "inline";
			spinner.style.display = "none";
		}
	);
}

function openUpdateRDModal(rd) {
	const selected_row = document.getElementById(rd);
	document.getElementById("rd-type-update").value =
		selected_row.children.item(0).innerHTML;

	document.getElementById("rd-id").value = rd;
	openModal("update-rd-modal");
}

async function update_radio_image_symtoms() {
	const type = document.getElementById("rd-type-update").value;

	if (!type) {
		showNotification("Please fill all fields!");
		return;
	}
	const rd_id = document.getElementById("rd-id").value;
	const btn = document.getElementById("submit-rd-btn-update");
	const text = document.getElementById("rd-submit-text-update");
	const spinner = document.getElementById("rd-submit-spinner-update");

	btn.disabled = true;
	text.style.display = "none";
	spinner.style.display = "inline-block";
	await _call(
		`/patient/radio-image/${rd_id}`,
		"PUT",
		{
			type,
		},
		(data) => {
			showNotification("Radio Image Type is updated Successfelly!", true);
			const selected_row = document.getElementById(rd_id);
			selected_row.children.item(0).innerHTML = type;
			btn.disabled = false;
			text.style.display = "inline";
			spinner.style.display = "none";
			document.getElementById("rd-id").value = "";
			closeModal("update-rd-modal");
		},
		() => {
			btn.disabled = false;
			text.style.display = "inline";
			spinner.style.display = "none";
		}
	);
}

async function check() {
	document.querySelectorAll("button").forEach((btn) => (btn.disabled = true));
	document.getElementById("loader").style.display = "flex";
	await _call(
		`/doctor/check/${id}`,
		"POST",
		undefined,
		(data) => {
			showNotification("Patient is checked!", true);
			fill_table_patient(data);
			document
				.querySelectorAll("button")
				.forEach((btn) => (btn.disabled = false));
			document.getElementById("loader").style.display = "none";
		},
		() => {
			document
				.querySelectorAll("button")
				.forEach((btn) => (btn.disabled = false));
			document.getElementById("loader").style.display = "none";
		}
	);
}
