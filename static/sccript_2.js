document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".edit-btn").forEach(button => {
        button.addEventListener("click", function () {
            let departmentId = this.getAttribute("data-department-id");

            fetch(`/get_department/${departmentId}`)
                .then(response => response.json())
                .then(data => {
                    // Заполняем форму
                    document.getElementById("department_id").value = data.id;
                    document.getElementById("edit_title").value = data.title;

                    let chiefSelect = document.getElementById("edit_chief");
                    if (chiefSelect) {
                        let chiefId = parseInt(data.chief[0]); // ID руководителя
                        for (let option of chiefSelect.options) {
                            option.selected = parseInt(option.value) === chiefId;
                        }
                    }

                    let membersSelect = document.getElementById("edit_members");
                    if (membersSelect) {
                        let selectedValues = data.members.map(user => user[0]);
                        for (let option of membersSelect.options) {
                            option.selected = selectedValues.includes(parseInt(option.value));
                        }
                    }

                    document.getElementById("edit_email").value = data.email;
                })
                .catch(error => console.error("Ошибка загрузки данных:", error));
        });
    });
});

document.addEventListener("DOMContentLoaded", function () {
    let addModal = document.getElementById("addDepartment");
    if (addModal) {
        addModal.addEventListener("hidden.bs.modal", function () {
            this.querySelector("form").reset();
        });
    }

    let editModal = document.getElementById("editDepartment");
    if (editModal) {
        editModal.addEventListener("hidden.bs.modal", function () {
            this.querySelector("form").reset();
        });
    }
});
