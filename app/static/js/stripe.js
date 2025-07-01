const stripe = Stripe('pk_test_51N9lt0DbeuwCoATIiZ3K2XVeeV5lOZgB7m0WY1G7Ul0s9as5vaU7dQTSZaPiJpzkvIeevRPkkorz1XndPt2B3CjG00IefeyTlL');
const elements = stripe.elements();

// 例: ページが読み込まれたときにクッキーを設定する
document.addEventListener('DOMContentLoaded', function() {
  document.cookie = "myCookie=myValue; samesite=strict";
});



// Custom styling can be passed to options when creating an Element.
// const style = {
//     base: {
//       // Add your base input styles here. For example:
//       fontSize: '16px',
//       color: '#32325d',
//     },
// };
// スタイルの定義
const style = {
  base: {
    color: "#32325d",
    fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
    fontSmoothing: "antialiased",
    fontSize: "16px",
    '::placeholder': {
      color: "#aab7c4"
    }
  },
  invalid: {
    color: "#fa755a",
    iconColor: "#fa755a"
  }
};

// カード要素の作成
const card = elements.create("card", { style: style });

// DOM にマウント
card.mount("#card-element");
  
// Create an instance of the card Element.
// const card = elements.create('card', {style});
  
// Add an instance of the card Element into the `card-element` <div>.
card.mount('#card-element');


// Create a token or display an error when the form is submitted.
const form = document.getElementById('payment-form');
form.addEventListener('submit', async (event) => {
  event.preventDefault();

  const {token, error} = await stripe.createToken(card);

  if (error) {
    // Inform the customer that there was an error.
    const errorElement = document.getElementById('card-errors');
    errorElement.textContent = error.message;
  } else {
    // Send the token to your server.
    stripeTokenHandler(token);
  }
});



const stripeTokenHandler = (token) => {
    // Insert the token ID into the form so it gets submitted to the server
    const form = document.getElementById('payment-form');
    const hiddenInput = document.createElement('input');
    hiddenInput.setAttribute('type', 'hidden');
    hiddenInput.setAttribute('name', 'stripeToken');
    hiddenInput.setAttribute('value', token.id);
    form.appendChild(hiddenInput);
  
    // Submit the form
    form.submit();
}