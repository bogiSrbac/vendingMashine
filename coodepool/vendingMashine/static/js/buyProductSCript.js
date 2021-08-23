const getProductId = document.querySelectorAll('.getProductId');
const buyProductClass = document.querySelectorAll('.buyProductClass');


let close3 = document.querySelector('.close3');
let close4 = document.querySelector('.close4');
let messageError = document.getElementById('error-text1');
let messageSuccess = document.getElementById('success-text1');


let updateBuy = document.getElementById('updateFormModal');
let formBuy = document.getElementById('formBuy');

const product_name = document.getElementById('id_product_name');
const user_buy = document.getElementById('id_user_buy');
const amount = document.getElementById('id_amount');
const buyProductButton = document.getElementById('buyProductButton');
const insertProductName = document.getElementById('insertProductName');
const prPk = document.getElementById('pk');

const navBarDeposit = document.getElementById('navBarDeposit');

// modal function bootstrap
function triggerModal() {
         $("#myModalBuy").modal('show');

}

// buy product function
function formBuyProduct() {
    formBuy.addEventListener('submit', e=>{
        e.preventDefault();
        const fbuyForm = new FormData();
        fbuyForm.append('csrfmiddlewaretoken', csrftoken1);
        fbuyForm.append('amount', amount.value);

        let fSubmitBuy = new XMLHttpRequest();
        fSubmitBuy.responseType = 'json';
        fSubmitBuy.enctype = 'multipart/form-data';
        fSubmitBuy.data = fbuyForm;
        let idUrl = prPk.innerText;
        let fURLDeposit = `/buy-product/${idUrl}`;
        fSubmitBuy.open('POST', fURLDeposit, true);
        fSubmitBuy.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
        fSubmitBuy.onload = function () {
            buyResponse = fSubmitBuy.response;


            if(buyResponse.error){
                messageError.innerHTML = buyResponse.error;
                triggerModal()
             }else if(buyResponse.message){
                messageError.innerHTML = buyResponse.message;
                insertProductName.innerHTML = '';
                amount.value = '';
                prPk.innerText = '';
                buyResponse.innerHTML = '';
                prPk.innerText = '';
                var nameFull1 = buyResponse['productName'];
                var amount1 = buyResponse['amountAvailable'];
                var cost1 = buyResponse['cost'];
                var pk1 = buyResponse['pk'];
                insertProductName.innerHTML += `${nameFull1} </br>On stock: ${amount1} </br> Cost: ${cost1}`;
                prPk.innerText = pk1;
                console.log(buyResponse)
                navBarDeposit.innerHTML = '';
                navBarDeposit.innerHTML = `${buyResponse.newDeposit} coins`;
                triggerModal()}

            close3.addEventListener('click', ()=>{
                messageError.innerText = '';
                messageSuccess.innerHTML = '';
            });
            close4.addEventListener('click', ()=>{
                messageError.innerText = '';
                messageSuccess.innerHTML = '';
            })



        };
        fSubmitBuy.send(fbuyForm);

    })
}


formBuyProduct()
//get product info

function buyProductInsertFunc() {
    for(let i = 0; i < buyProductClass.length; i++){
        buyProductClass[i].addEventListener('click', ()=>{
            let productId = getProductId[i].innerText;
            const xhrNew = new XMLHttpRequest();
            xhrNew.responseType = 'json';
            xhrNew.enctype = 'multipart/form-data';
            let fURLproduct = `/get-products-data/${productId}`;
            xhrNew.open('GET', fURLproduct, true);
            xhrNew.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
            let htmlPro = '';
            xhrNew.onload = function () {
                productInfo = xhrNew.response;
                insertProductName.innerHTML = '';
                prPk.innerText = '';
                var nameFull = productInfo['productName'];
                var amount = productInfo['amountAvailable'];
                var cost = productInfo['cost'];
                var pk = productInfo['pk'];
                insertProductName.innerHTML += `${nameFull} </br>On stock: ${amount} </br> Cost: ${cost}`;
                prPk.innerText = pk;

                 triggerModal()
            };
            xhrNew.send();
                })
    }
}
buyProductInsertFunc()


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
const csrftoken1 = getCookie('csrftoken');