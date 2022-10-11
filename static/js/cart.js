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
            console.log('User is not currently authenticated')
                    
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