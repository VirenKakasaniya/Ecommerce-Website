console.log("hello world");

var updateBtns = document.getElementsByClassName('update-cart')

for (i = 0; i < updateBtns.length; i++){
    updateBtns[i].addEventListener('click', function(){
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('productId:',productId,'Action:',action)

        console.log('USER:',user)
        if(user == 'AnonymousUser'){
            console.log('Not logged in'),
        
            // var url =  "{% url 'Account:login' %}";
            // window.location.href =  'Account/loginpage/';
            window.location.href =  url;

            
            
        }else{
            updateUserOrder(productId, action)
            
        }
    })
}

function updateUserOrder(productId, action){
    console.log('user is logged in, sending data...')

    var url = '/update_Item/'
    

    fetch(url, {
        method : 'POST',
        headers: {
            'Content-Type':'application/json',
            // 'Accept': 'application/json',
            'X-CSRFToken' : csrftoken,
        },
        body:JSON.stringify({'productId':productId,'action':action})
    })

    .then((respnose) => {
        return respnose.json()
    })

    .then((data) => {
        console.log('data: ',data) 
        location.reload()
    })
}