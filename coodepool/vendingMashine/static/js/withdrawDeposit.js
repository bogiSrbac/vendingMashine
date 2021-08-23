const getUserId = document.getElementById('getUserId').innerText;
const resetDeposit = document.getElementById('resetDeposit');
const list_group = document.getElementById('list-group');



function withdrawDeposit() {
    resetDeposit.addEventListener('click', ()=>{
    list_group.innerHTML = '';
    let confirmReset = confirm('Are you sure to withdraw deposit?');
    if(confirmReset){
        let resetDepositXHR = new XMLHttpRequest();
        resetDepositXHR.responseType = 'json';
        resetDepositXHR.enctype = 'multipart/form-data';
        let fURLreset = `/withdraw-deposit/${getUserId}/`;
        resetDepositXHR.open('PUT', fURLreset, true);
        resetDepositXHR.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
        resetDepositXHR.setRequestHeader("X-CSRFToken", csrftoken);
        let htmlReset = '';
        resetDepositXHR.onload = function () {
            resetDEpositData = resetDepositXHR.response;


            for(let key in resetDEpositData.coins){
                if(resetDEpositData.coins[key] > 0 ){
                htmlReset += ` <li class="list-group-item d-flex justify-content-between align-items-center">Amount of coin ${key}`;
                htmlReset += `<span class="badge badge-primary badge-pill">${resetDEpositData.coins[key]} coins</span></li>`;
            }

            }

            list_group.innerHTML += htmlReset;
            navBarDeposit.innerHTML = `0 coins`;

            if(resetDEpositData.error){
                messageError.innerHTML = resetDEpositData.error;
                triggerModal()
             }else if(resetDEpositData.update){
                messageError.innerHTML = resetDEpositData.update;
                triggerModal()}

            close.addEventListener('click', ()=>{
                messageError.innerText = '';
                messageSuccess.innerHTML = '';
            });
            close2.addEventListener('click', ()=>{
                messageError.innerText = '';
                messageSuccess.innerHTML = '';
            })

        };
        resetDepositXHR.send();
    }

})
}
if(sowSeller === '2'){
      withdrawDeposit()
}
