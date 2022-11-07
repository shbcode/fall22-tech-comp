var updateButtons = document.getElementsByClassName('updatecart')
console.log("hi console reader")
console.log(updateButtons.length)
for (var l = 0; l < updateButtons.length; l++) {
    console.log("button updated")
    updateButtons[l].addEventListener('click', function(){
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('Product Id: ', productId, 'Action: ', action)
        console.log('USER:', user)
        if (user == 'AnonymousUser'){
            console.log("It's anonymous")
            addCookieItem(productId, action)
        }else{
            updateUserOrder(productId, action)
        }
            })
}
function updateUserOrder(productId, action){
    console.log('User is authenticated, sending the data')
        var url = '/store/update_item/'
        fetch(url, {
            method:'POST',
            headers:{
                'Content-Type':'application/json',
                'X-CSRFToken':csrftoken,
            }, 
            body:JSON.stringify({'productId':productId, 'action':action})
        })
        .then((response) => {
            return response.json();
        })
        .then((data) => {
            location.reload() // page reloads once call is successful which is a bit taxing but works effectively
        });
}

function addCookieItem(productId, action){
    console.log('User is not authenticated')
    console.log("NEWFUNCTIONHAPPENED")
    console.log("ProductId:", productId)
    console.log("Action:", action)
    if (action == 'add'){
        if (cart[productId] == undefined){
            cart[productId] = {"quantity":1}
        }else{
            cart[productId]["quantity"] += 1
        }
    }

    if (action == 'remove'){
        cart[productId]["quantity"] -= 1
        if (cart[productId]["quantity"] <= 0){
            console.log("Item needs to be deleted")
            delete cart[productId];
        }
    }
    console.log("Cart:", cart)
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
    location.reload()
}