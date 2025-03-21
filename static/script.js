document.addEventListener("DOMContentLoaded", function () {
        document.querySelectorAll(".edit-btn").forEach(button => {
            button.addEventListener("click", function () {
                let jobId = this.getAttribute("data-job-id");

                fetch(`/get_job/${jobId}`)
                    .then(response => response.json())
                    .then(data => {
                        // Заполняем форму
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

                        var myModal = new bootstrap.Modal(document.getElementById('edit_job'));
                        myModal.show();
                    })
                    .catch(error => console.error("Ошибка загрузки данных:", error));
            });
        });
    });