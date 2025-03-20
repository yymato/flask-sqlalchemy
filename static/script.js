document.addEventListener("DOMContentLoaded", function () {
        document.querySelectorAll(".edit-btn").forEach(button => {
            button.addEventListener("click", function () {
                let jobId = this.getAttribute("data-job-id");

                fetch(`/get_job/${jobId}`)
                    .then(response => response.json())
                    .then(data => {
                        // Заполняем форму
                        document.getElementById("edit_job_id").value = data.id;
                        document.getElementById("edit_team_leader").value = data.team_leader;
                        document.getElementById("edit_job_job").value = data.job;
                        document.getElementById("dit_job_worksize").value = data.worksize
                        document.getElementById("edit_job_collaborators").value = data.collaboration
                        var myModal = new bootstrap.Modal(document.getElementById('edit_job'));
                        myModal.show();
                    })
                    .catch(error => console.error("Ошибка загрузки данных:", error));
            });
        });
    });