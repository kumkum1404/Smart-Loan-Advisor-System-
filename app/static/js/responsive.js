const menuBtn=document.querySelector(".menu-toggle");

const sidebar=document.querySelector(".sidebar");

if(menuBtn){

menuBtn.onclick=function(){

sidebar.classList.toggle("active");

}

}