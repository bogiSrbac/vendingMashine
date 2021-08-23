// const addPurchases = document.getElementById('addPurchases');
//
//
// function allPurchases() {
//     let xhrPurch = new XMLHttpRequest();
//     xhrPurch.responseType = 'json';
//     xhrPurch.enctype = 'multipart/form-data';
//     let fURLnewPurch = '/all-products-xhr/';
//     xhrPurch.open('GET', fURLnewPurch, true);
//     xhrPurch.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
//     let htmlPurch = '';
//     xhrPurch.onload = function () {
//                     productPurch = xhrPurch.response;
//                     for(let key in productPurch){
//                         for( let key1 in productPurch[key]){
//                             htmlPurch +=`<div class="container text-left border border-secondary rounded mb-2 align-self-start buyProductClass" style="width: 17rem">`
//                             htmlPurch += `<p class="getProductId" style="display: none">${productPurch[key][key1]['id']}</p>`
//                             htmlPurch += `<ul class="list-group list-group-flush">`;
//                             htmlPurch += `<li class="list-group-item">Product name: ${productPurch[key][key1]['productName']}</li>
//                                     <li class="list-group-item">Seller: ${productPurch[key][key1]['user_product__username']}</li>
//                                     <li class="list-group-item">Amount available: ${productPurch[key][key1]['amountAvailable']}</li>
//                                     <li class="list-group-item">Cost: ${productPurch[key][key1]['cost']}</li></ul></div>`
//                         }
//                     }
//                     buyProductInsertFunc();
//                     formBuyProduct()
//
//                     addPurchases.innerHTML = '';
//                     addPurchases.innerHTML = htmlPurch
//
//     };
//     xhrPurch.send();
// }
// setTimeout(function () {
//     allPurchases()
//     intervaPurch = setInterval(function () {
//         allPurchases()
//     }, 10000)
// }, 1000)
//
//
