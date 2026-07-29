document.addEventListener("DOMContentLoaded", function(){


    const toggleBtn = document.querySelector(".mobile-toggle");

    const sidebar = document.querySelector(".sidebar");


    if(toggleBtn && sidebar){


        toggleBtn.addEventListener("click", function(){


            sidebar.classList.toggle("active");


        });


    }



    // sidebar close when clicking outside

    document.addEventListener("click", function(event){


        if(window.innerWidth <= 992){


            if(
                sidebar &&
                !sidebar.contains(event.target) &&
                !toggleBtn.contains(event.target)
            ){

                sidebar.classList.remove("active");

            }


        }


    });



});