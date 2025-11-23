const patient_info_table = document.getElementById("patient-info");
fill_info() ;
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
    const id = document.getElementById('patient-id').value
	_call(
		"/patient/"+id,
		"GET",
		undefined,
		(data) => {
			fill_table_patient(data);
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
