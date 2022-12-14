

/* toggle navbar */

const menubtn = document.querySelector("#menu-btn");
const navBbar = document.querySelector(".nav-bar");


menubtn.addEventListener('click', () => {
    menubtn.classList.toggle("active");
    navBbar.classList.toggle("active");
})

const navToggler = document.querySelector(".nav-toggler");
navToggler.addEventListener("click",toggleNav);

function toggleNav(){
    navToggler.classList.toggle("active");
    document.querySelector(".nav").classList.toggle("open");

} 



/* close nav when click */


document.addEventListener("click",function(e){
    if(e.target.closest(".nav-item")){ 
        toggleNav();
    }
})

/* close search-form when click */

document.querySelector('#search-btn').onclick = () =>{
    document.querySelector('#search-form').classList.toggle('active');
}

document.querySelector('#close').onclick = () =>{
    document.querySelector('#search-form').classList.remove('active');
}


/* sticky */


window.addEventListener("scroll",function(){
    if(this.pageYOffset > 60){
        document.querySelector(".header").classList.add("sticky");

    }
    else {
        document.querySelector(".header").classList.remove("sticky");

    }
});


let shoppingcart = document.querySelector('.shopping-cart');

document.querySelector('#cart-btn').onclick = () =>{
    shoppingcart.classList.toggle('active');
    navBar.classList.remove('active');
    loginForm.classList.remove('active');
}

let loginForm = document.querySelector('.login-form');

document.querySelector('#login-btn').onclick = () =>{
    loginForm.classList.toggle('active');
    navBar.classList.remove('active');
    shoppingcart.classList.remove('active');
}

let navBar = document.querySelector('.nav-bar');

document.querySelector('#menu-btn').onclick = () =>{
    navBar.classList.toggle('active');
    shoppingcart.classList.remove('active');
    loginForm.classList.remove('active');
}

let section = document.querySelectorAll('section');
let navLinks = document.querySelectorAll('header .nav-bar a');
let footer = document.querySelectorAll('footer');
window.onscroll = () =>{

    
    shoppingcart.classList.remove('active');
    loginForm.classList.remove('active');
   
    section.forEach(sec =>{

        let top = window.scrollY;
        let offset = sec.offsetTop - 500;
        let height = sec.offsetHeight;
        let id = sec.getAttribute('id');

        if (top >= offset && top < offset + height){
            navLinks.forEach(links =>{
                links.classList.remove('active');
                document.querySelector('header .nav-bar a[href*=' + id + ']').classList.add('active');
            })
        }
    })

    footer.forEach(sec =>{
        let top = window.scrollY;
        let offset = sec.offsetTop - 700;
        let height = sec.offsetHeight;
        let id = sec.getAttribute('id');

        if (top >= offset && top < offset + height){
            navLinks.forEach(links =>{
                links.classList.remove('active');
                document.querySelector('header .nav-bar a[href*=' + id + ']').classList.add('active');
            })
        }

    })
}

/* ---------------- menu tabs -------------- */

const menuTabs = document.querySelector(".menu-tabs");
menuTabs.addEventListener("click", function(e){
    if(e.target.classList.contains("menu-tab-item") && !e.target.classList.contains("active")){
        const target = e.target.getAttribute("data-target");
        menuTabs.querySelector(".active").classList.remove("active");
        e.target.classList.add("active");
        const menuSection = document.querySelector(".menu-section");
        menuSection.querySelector(".menu-tab-content.active").classList.remove("active");
        menuSection.querySelector(target).classList.add("active");
    }
});
/* -------------------------------- */





