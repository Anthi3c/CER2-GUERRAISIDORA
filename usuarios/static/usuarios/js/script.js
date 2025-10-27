
//Sacado de w3schools

//Hero de la página principal

//Fecha de inicio del evento
var countDownDate = new Date("Sep 09, 2025 16:00:00").getTime()

//Más detalles

function masDetalles() {
  var popup = document.getElementById("myPopup");
  popup.classList.toggle("show");
}

var x = setInterval(function(){

    var now = new Date().getTime();

    //countdown
    var distance = countDownDate - now;
    
    var days = Math.floor(distance / (1000 * 60 * 60 * 24));
    var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
    var seconds = Math.floor((distance % (1000 * 60)) / 1000);
        
    document.getElementById("fecha").innerHTML = days + "d " + hours + "h "
    + minutes + "m " + seconds + "s ";

    if (distance < 0) {
        clearInterval(x);
        document.getElementById("fecha").innerHTML = "¡EL EVENTO HA COMENZADO!";
    }
}, 1000);

//Comunidad

const userId = {
    name: null,
    message: null,
    date:null
}

const userComment = document.querySelector(".usercomment")
const publishBtn = document.querySelector("#publish")
const comments = document.querySelector("#comentarios")
const userName = document.querySelector(".user")


function addPost(){
    if(!userComment.value) return
    userId.name=userName.value
    userId.message=userComment.value
    userId.date=new Date().toLocaleString()
    let published=`
    <div class="card">
        <div class="hol">
            <h3 class="nom">${userId.name}<h3>
            <p class="com">${userId.message}</p>
            <span class="date">${userId.date}</span>
        </div>
    </div>`

    comments.innerHTML += published
    userComment.value =""
}

publishBtn.addEventListener("click", addPost)