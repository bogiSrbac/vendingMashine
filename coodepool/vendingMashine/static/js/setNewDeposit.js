const formInsertDeposit = document.getElementById('formInsertDeposit');
const user_deposit = document.getElementById('id_user_deposit');
const add_deposit = document.getElementById('id_add_deposit');
const navBarDeposit = document.getElementById('navBarDeposit');
function formSetNewDeposit() {
    formInsertDeposit.addEventListener('submit', e=>{
        console.log('test1')
        e.preventDefault();
        const fdepositXHR = new FormData();
        fdepositXHR.append('csrfmiddlewaretoken', csrftoken);
        fdepositXHR.append('user_deposit', user_deposit.value);
        fdepositXHR.append('add_deposit', add_deposit.value);

        let fSubmitDeposit = new XMLHttpRequest();
        fSubmitDeposit.responseType = 'json';
        fSubmitDeposit.enctype = 'multipart/form-data';
        fSubmitDeposit.data = fdepositXHR;
        let fURLDeposit = '/set-deposit/';
        fSubmitDeposit.open('POST', fURLDeposit, true);
        fSubmitDeposit.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
        fSubmitDeposit.onload = function () {
            depositData = fSubmitDeposit.response;
            add_deposit.value = '';
            navBarDeposit.innerHTML = `${depositData.newDeposit} coins`;
            if(depositData.error){
                messageError.innerHTML = depositData.error;
                triggerModal()
             }else if(depositData.message){
                messageError.innerHTML = depositData.message;
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
        fSubmitDeposit.send(fdepositXHR);

    })
}


if(sowSeller === '2'){
      formSetNewDeposit()
}
