document.addEventListener("DOMContentLoaded", function(){
    var modal = document.getElementById("myModal");
    var display_imgs = document.getElementsByClassName("display_img")
    var span = document.getElementsByClassName("close")[0];
    var add_item_buttons = document.getElementsByClassName("add_item_button");

    for(i = 0; i < display_imgs.length; i++){
        display_imgs[i].onclick = function() {
            modal.style.display = "block";
            console.log(this.getAttribute('product_id'));
            fetch('/details/'+this.getAttribute('product_id'))
                .then(data => data.json())
                .then(data => {
                    console.log(data)
                    span.innerHTML =`
                    <p>Name: ${data.name}</p>
                    <p>Price: ${data.price}</p>
                    <p>Description ${data.desc}</p>
                    <img src="../static/pictures/${data.image}">
                    `
                })
        }
    }

    for(i = 0; i < add_item_buttons.length; i++) {
        add_item_buttons[i].onclick = function() {
            prod_id = this.getAttribute('product_id')
            amount = document.getElementById('add_item_selection_'+prod_id).value;
            fetch('/add_item/'+prod_id+'/'+amount)
                .then(data => data.json())
                .then(data => {
                    console.log(data)
                    document.getElementById('cart_item_count').innerHTML = data.items_in_cart
                })
        }
    }

    span.onclick = function() {
        modal.style.display = "none";
    }
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }
})