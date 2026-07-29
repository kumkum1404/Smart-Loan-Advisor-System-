// document.addEventListener("DOMContentLoaded", function(){



// const loanInput = document.querySelectorAll(
//     'input[type="range"]'
// );


// const loanAmount = document.querySelector(
//     ".input-group-box:nth-child(1) .value-box input"
// );


// const interestRate = document.querySelector(
//     ".input-group-box:nth-child(2) .value-box input"
// );


// const tenure = document.querySelector(
//     ".input-group-box:nth-child(3) .value-box input"
// );




// const emiResult = document.querySelector(
//     ".summary-box:nth-of-type(1) h2"
// );


// const interestResult = document.querySelector(
//     ".summary-box:nth-of-type(2) h2"
// );


// const totalResult = document.querySelector(
//     ".summary-box:nth-of-type(3) h2"
// );


// const circleAmount = document.querySelector(
//     ".circle-chart strong"
// );





// function calculateEMI(){



//     let P =
//     Number(loanAmount.value);



//     let yearlyRate =
//     Number(interestRate.value);



//     let years =
//     Number(tenure.value);



//     let N = years * 12;



//     let R =
//     yearlyRate / 12 / 100;



//     let EMI;



//     if(R === 0){

//         EMI = P / N;

//     }

//     else{


//         EMI =
//         P * R *
//         Math.pow(1+R,N)
//         /
//         (Math.pow(1+R,N)-1);


//     }





//     let totalPayment =
//     EMI * N;


//     let totalInterest =
//     totalPayment - P;




//     emiResult.innerHTML =
//     "₹" +
//     Math.round(EMI)
//     .toLocaleString("en-IN");



//     interestResult.innerHTML =
//     "₹" +
//     Math.round(totalInterest)
//     .toLocaleString("en-IN");



//     totalResult.innerHTML =
//     "₹" +
//     Math.round(totalPayment)
//     .toLocaleString("en-IN");



//     circleAmount.innerHTML =
//     "₹" +
//     Math.round(totalPayment)
//     .toLocaleString("en-IN");



// }





// // slider update


// loanInput.forEach((slider,index)=>{


// slider.addEventListener(
// "input",
// function(){


// if(index===0){

// loanAmount.value=this.value;

// }


// if(index===1){

// interestRate.value=this.value;

// }


// if(index===2){

// tenure.value=this.value;

// }


// calculateEMI();


// });


// });




// // manual input change


// [
// loanAmount,
// interestRate,
// tenure

// ].forEach(input=>{


// input.addEventListener(
// "input",
// calculateEMI
// );


// });




// // initial calculation

// calculateEMI();



// });


document.addEventListener("DOMContentLoaded", function () {


    const calculateBtn = document.getElementById("calculateEMI");


    calculateBtn.addEventListener("click", function () {


        let principal = 
        parseFloat(document.getElementById("loanAmount").value);


        let annualRate = 
        parseFloat(document.getElementById("interestRate").value);


        let years = 
        parseFloat(document.getElementById("tenure").value);



        if(!principal || !annualRate || !years){

            alert("Please enter all loan details");

            return;

        }



        // Monthly interest rate

        let monthlyRate = annualRate / 12 / 100;


        // Total months

        let months = years * 12;



        // EMI Formula

        let emi = 
        (principal * monthlyRate * Math.pow(1 + monthlyRate, months)) /
        (Math.pow(1 + monthlyRate, months) - 1);



        let totalPayment = emi * months;


        let totalInterest = totalPayment - principal;



        // Round values

        emi = Math.round(emi);

        totalPayment = Math.round(totalPayment);

        totalInterest = Math.round(totalInterest);



        // Update UI


        document.getElementById("monthlyEMI").innerHTML =
        "₹" + emi.toLocaleString("en-IN");



        document.getElementById("totalInterest").innerHTML =
        "₹" + totalInterest.toLocaleString("en-IN");



        document.getElementById("totalPayment").innerHTML =
        "₹" + totalPayment.toLocaleString("en-IN");



        document.getElementById("payableAmount").innerHTML =
        "₹" + totalPayment.toLocaleString("en-IN");



    });



});