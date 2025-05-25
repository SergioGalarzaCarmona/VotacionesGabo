const select = document.getElementById('open-dialog');
select.addEventListener('click', validateGroup)
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
    const subusersTable = document.querySelector('.subusers-table__container');
    const closeFormGroup = document.querySelector(".close-formGroup");
    const closeFormSubuser = document.querySelector(".close-formSubuser");

    function toggleTableVisibility() {
        if (create_subuser.checked) {
            subusersTable.classList.add("hidden");
            closeFormGroup.classList.add("hidden");
            closeFormSubuser.classList.remove("hidden");
        } 
        else if (create_candidate.checked) {
            subusersTable.classList.add("hidden");
            closeFormSubuser.classList.add("hidden");
            closeFormGroup.classList.remove("hidden");
        }
        else {
            subusersTable.classList.remove("hidden");
            closeFormGroup.classList.add("hidden");
            closeFormSubuser.classList.add("hidden");
        }
    }

    create_subuser.addEventListener("change", toggleTableVisibility);
    create_candidate.addEventListener("change", toggleTableVisibility);
    
    toggleTableVisibility();
});