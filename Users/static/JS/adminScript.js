const label_candidate = document.querySelector('.create-candidate-label');
const label_subuser = document.querySelector('.create-subuser-label');
const create_candidate = document.getElementById('create-candidate');
const create_subuser = document.getElementById('create-subuser');
label_candidate.addEventListener('click', function (){
    create_subuser.checked = false; 
});
label_subuser.addEventListener('click', function (){
    create_candidate.checked = false;
});

document.addEventListener("DOMContentLoaded", () => {
    const resultados = document.querySelector('.resultados');
    const closeFormCandidate = document.querySelector(".close-formCandidate");
    const closeFormSubuser = document.querySelector(".close-formSubuser");

    function toggleTableVisibility() {
        if (create_subuser.checked) {
            resultados.classList.add("hidden");
            closeFormCandidate.classList.add("hidden");
            closeFormSubuser.classList.remove("hidden");
        } 
        else if (create_candidate.checked) {
            resultados.classList.add("hidden");
            closeFormSubuser.classList.add("hidden");
            closeFormCandidate.classList.remove("hidden");
        }
        else {
            resultados.classList.remove("hidden");
            closeFormCandidate.classList.add("hidden");
            closeFormSubuser.classList.add("hidden");
        }
    }

    create_subuser.addEventListener("change", toggleTableVisibility);
    create_candidate.addEventListener("change", toggleTableVisibility);
    
    toggleTableVisibility();
});

const dialog = document.querySelector(".reset-dialog");
const openDialog = document.querySelector(".open-dialog");
openDialog.addEventListener("click", () => {
    dialog.showModal();
});
const closeDialog = document.getElementById("close-dialog");
closeDialog.addEventListener("click", () => {
    dialog.close();
});