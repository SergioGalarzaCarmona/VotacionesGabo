const select = document.getElementById('open-dialog');
select.addEventListener('click', validateGroup)
const label_group = document.querySelector('.create-group-label');
const label_subuser = document.querySelector('.create-subuser-label');
const create_group = document.getElementById('create-group');
const create_subuser = document.getElementById('create-subuser');
label_group.addEventListener('click', function (){
    create_subuser.checked = false; 
});
label_subuser.addEventListener('click', function (){
    create_group.checked = false;
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
        else if (create_group.checked) {
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
    create_group.addEventListener("change", toggleTableVisibility);
    
    toggleTableVisibility();
});