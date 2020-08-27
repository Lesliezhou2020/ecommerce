document.addEventListener("DOMContentLoaded", function(){
    var modal = document.getElementById("myModal");
    var display_imgs = document.getElementsByClassName("display_img")
    var span = document.getElementsByClassName("close")[0];

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

    span.onclick = function() {
        modal.style.display = "none";
    }
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }
})