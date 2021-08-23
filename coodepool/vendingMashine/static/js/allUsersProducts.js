const loopUserProducts = document.getElementById('loopUserProducts')
const submitProduct = document.getElementById('submitProduct')
const costUpdate = document.getElementById('cost');
const amount = document.getElementById('amount');
const nameUpdate = document.getElementById('name');


const formUpdateProduct = document.getElementById('formUpdateProduct')


function getProductData() {
    let xhr1 = new XMLHttpRequest();
    xhr1.responseType = 'json';
    xhr1.enctype = 'multipart/form-data';
    let fURLnew1 = '/user-products/';
    xhr1.open('GET', fURLnew1, true);
    xhr1.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    let html1 = '';
    xhr1.onload = function () {
                    productData1 = xhr1.response;
                    for(let i = 0; i < productData1.data.length; i++){
                        var obj1 = productData1.data[i]
                        html1 += `<li class="list-group-item"><span class="text-primary">${productData1.username}:</span> Product name: ${obj1.productName}, Amount available: ${obj1.amountAvailable}, Cost: ${obj1.cost}<button type="button" class="btn btn-outline-warning btn-sm ml-2 getUpdate"><span class="getUpdateID" style="display: none">${obj1.id}</span>Update</button><button type="button" class="btn btn-outline-danger btn-sm ml-2 getDelete"><span class="getDeleteID" style="display: none">${obj1.id}</span>Delete</button></li>`
                    }
                    loopUserProducts.innerText = '';
                    loopUserProducts.innerHTML += html1
                    updateFunction()
                    deleteProductFunction()
    };
    xhr1.send();
}



if(sowSeller === '1'){
  setTimeout(function () {
    intervalProducts = setInterval(function () {
        getProductData()
    }, 3000)

}, 500)
}




function updateFunction() {
    let getUpdateID = document.querySelectorAll('.getUpdateID');
    let getUpdate = document.querySelectorAll('.getUpdate');


    for(let j = 0; j < getUpdate.length; j++){
        //if statment for update product

            getUpdate[j].addEventListener('click', ()=>{
            let idUpdate = getUpdateID[j].innerHTML;
            formUpdateProduct.style.display = 'block';

            var objUpdate = productData1.data[j];
            costUpdate.value = objUpdate.cost;
            amount.value = objUpdate.amountAvailable;
            nameUpdate.value = objUpdate.productName;
            triggerModal()
            formUpdateProduct.addEventListener('submit', e=>{
                e.preventDefault();
                formUpdateProduct.style.display = 'none';
                let fUpdateForm = new FormData();
                fUpdateForm.append('csrfmiddlewaretoken', csrftoken);
                fUpdateForm.append('cost', costUpdate.value);
                fUpdateForm.append('amount', amount.value);
                fUpdateForm.append('name', nameUpdate);
                let fSubimtUpdate = new XMLHttpRequest();
                fSubimtUpdate.responseType = 'json';
                fSubimtUpdate.enctype = 'multipart/form-data';
                fSubimtUpdate.data = fUpdateForm;
                let fURLUpdate = `/user-products-update/${idUpdate}/`;
                fSubimtUpdate.open('POST', fURLUpdate, true);
                fSubimtUpdate.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
                fSubimtUpdate.onload = function () {
                    dataUpdateProduct = fSubimtUpdate.response;

                    if(dataUpdateProduct.error){
                        messageError.innerHTML = dataUpdateProduct.error;
                        triggerModal()
                     }else if(dataUpdateProduct.update){
                        messageError.innerHTML = dataUpdateProduct.update;
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
                fSubimtUpdate.send(fUpdateForm);
                        })
    })
}
}


function deleteProductFunction(){
    let getDeleteID = document.querySelectorAll('.getDeleteID');
    let getDelete = document.querySelectorAll('.getDelete');
    for(let c = 0; c < getDelete.length; c++){
        //if statment for update product

        getDelete[c].addEventListener('click', ()=>{
        let idDelete = getDeleteID[c].innerHTML;
        let confirmDelete = confirm(`Are you sure to want to delete this product?`);
        if(confirmDelete){
            let fDelete = new XMLHttpRequest();
            fDelete.responseType = 'json';
            fDelete.enctype = 'multipart/form-data';
            let fURLDelete = `/user-products-delete/${idDelete}/`;

            fDelete.open('DELETE', fURLDelete, true);
            fDelete.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
            fDelete.setRequestHeader("X-CSRFToken", csrftoken);
            fDelete.onload = function () {
                dataDeleteProduct = fDelete.response;

                if(dataDeleteProduct.error){
                    messageError.innerHTML = dataDeleteProduct.error;
                    triggerModal()
                 }else if(dataDeleteProduct.update){
                    messageError.innerHTML = dataDeleteProduct.update;
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
        fDelete.send();
        }


    })
}



}

window.addEventListener('visibilitychange', function () {
                if(document.hidden){
                    clearInterval(intervalProducts);
                    loopUserProducts.innerHTML = ''
                }else {
                    if(sowSeller === '1'){
                          setTimeout(function () {
                            intervalProducts = setInterval(function () {
                                getProductData()
                            }, 3000)

                        }, 500)
                        }
                }
            });