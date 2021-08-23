const formAddProductId = document.getElementById('formAddProduct');
const productName = document.getElementById('id_productName');
const amountAvailable = document.getElementById('id_amountAvailable');
const cost = document.getElementById('id_cost');
let close = document.querySelector('.close');
let close2 = document.querySelector('.close2');
const user_product = document.getElementById('id_user_product');
let messageError = document.getElementById('error-text');
let messageSuccess = document.getElementById('success-text');
const hiddenProdutct = document.querySelector('#hiddenProdutct');
const sowSeller = hiddenProdutct.innerText;


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');


function formCreateNewProduct() {
    formAddProductId.addEventListener('submit', e=>{
        e.preventDefault();
        console.log('test1');
        const fproductXHR = new FormData();
        fproductXHR.append('csrfmiddlewaretoken', csrftoken);
        fproductXHR.append('user_product', user_product.value);
        fproductXHR.append('productName', productName.value);
        fproductXHR.append('amountAvailable', amountAvailable.value);
        fproductXHR.append('cost', cost.value);
        let fSubmitXHR = new XMLHttpRequest();
        fSubmitXHR.responseType = 'json';
        fSubmitXHR.enctype = 'multipart/form-data';
        fSubmitXHR.data = fproductXHR;
        let fURL = '/add-product/';
        fSubmitXHR.open('POST', fURL, true);
        fSubmitXHR.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
        console.log('test2');
        fSubmitXHR.onload = function () {
            dataF = fSubmitXHR.response;
            console.log('test3');
            productName.value = '';
            cost.value = '';
            amountAvailable.value = '';

            if(dataF.error){
                messageError.innerHTML = dataF.error;
                triggerModal()
             }else if(dataF.message){
                messageError.innerHTML = dataF.message;
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
        fSubmitXHR.send(fproductXHR);

    })
}
if(sowSeller === '1'){
    formCreateNewProduct();
}

// modal function bootstrap
function triggerModal() {
         $("#myModal").modal('show');

}