document.addEventListener("DOMContentLoaded", function () {
        document.querySelectorAll(".edit-btn").forEach(button => {
            button.addEventListener("click", function () {
                let jobId = this.getAttribute("data-job-id");

                fetch(`/get_job/${jobId}`)
                    .then(response => response.json())
                    .then(data => {
                        // Заполняем форму
                       document.getElementById("job_id").value = data.id
                       document.getElementById("edit_job_job").value = data.job;
                       document.getElementById("edit_job_worksize").value = data.worksize;

                        let teamLeaderSelect = document.getElementById("edit_job_leader");
                    if (teamLeaderSelect) {
                        let leaderId = parseInt(data.team_leader[0]); // ID лидера
                        for (let option of teamLeaderSelect.options) {
                            option.selected = parseInt(option.value) === leaderId;
                        }
                    }
                        let collaboratorsSelect = document.getElementById("edit_job_collaborators");
                        if (collaboratorsSelect) {
                            let selectedValues = data.collaboration.map(user => user[0]);
                            for (let option of collaboratorsSelect.options) {
                                option.selected = selectedValues.includes(parseInt(option.value));
                            }
                        }
                    })
                    .catch(error => console.error("Ошибка загрузки данных:", error));
            });
        });
    });


document.addEventListener("DOMContentLoaded", function () {
    let addJobModal = document.getElementById("addJob");
    addJobModal.addEventListener("hidden.bs.modal", function () {
        this.querySelector("form").reset();
    });
});

document.addEventListener("DOMContentLoaded", function () {
    let addJobModal = document.getElementById("editJob");
    addJobModal.addEventListener("hidden.bs.modal", function () {
        this.querySelector("form").reset();
    });
});