const paymentForm = document.getElementById('paymentForm');
paymentForm.addEventListener("submit", payWithPaystack, false);
function payWithPaystack(e) {
  e.preventDefault();

  let handler = PaystackPop.setup({
      key: 'pk_live_df1e9b848eb78b0c7bbd0510c446cdbdf639dcf4', // Replace with your public key
      email: document.getElementById("email-address").value,
      amount: document.getElementById("amount").value * 100,
      ref: ''+Math.floor((Math.random() * 1000000000) + 1), // generates a pseudo-unique reference. Please replace with a reference you generated. Or remove the line entirely so our API will generate one for you
      // label: "Optional string that replaces customer email"
      onClose: function(){
        let loader = document.querySelector("#loader")
        loader.style.display = "none";
      },
      callback: function(response){
        $.ajax({
            url: 'http://www.yoururl.com/verify_transaction?reference='+ response.reference,
            method: 'get',
            success: function (_response) {
              // the transaction status is in response.data.status
            }
          }); 
          
          window.location.assign("support-confirmpage.html");
      }
  });

  handler.openIframe();
}
