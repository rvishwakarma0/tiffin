var updateBtns = document.getElementsByClassName('update-cart')

for(i=0; i<updateBtns.length;i++){
    updateBtns[i].addEventListener('click',function(){
        var ProductId = this.dataset.product
        var action = this.dataset.action
        console.log('productId:',ProductId,'action:',action)

        console.log('user:',user)
        if (user === 'AnonymousUser') {
            addCookieItem(ProductId, action)
        }
        else{
            UpdateUserOrder(ProductId, action)
        }
    })
}

function addCookieItem(ProductId, action){
    console.log("not logged in")
    if(action == 'add'){
        if(cart[ProductId]== undefined){
            cart[ProductId]={'quantity':1}
        }
        else{
            cart[ProductId]['quantity'] +=1
        }
    }
    if(action == 'remove'){
        cart[ProductId]['quantity'] -= 1
        if(cart[ProductId]['quantity']<=0){
            console.log('item should be deleted')
            delete cart[ProductId];
        }
    }
    console.log('cart:',cart)
    document.cookie = 'cart=' + JSON.stringify(cart) + ';domain=;path=/'
    location.reload()
}

function UpdateUserOrder(ProductId, action){
    console.log('User is logged in, sending data... ')

    var url='/update_item/'
    fetch(url, {
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({'ProductId':ProductId, 'action':action})
    })

    .then((response)=>{
        return response.json()
    })

    .then((data)=>{
        console.log('data', data)
        location.reload()
    })
}