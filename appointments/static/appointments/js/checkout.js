const stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);
const clientSecret = $('#id_client_secret').text().slice(1, -1);
const stripe = Stripe(stripePublicKey);
const bookingIdElement = document.getElementById('id_appointment_id');
const bookingIdValue = bookingIdElement.textContent;
const bookingId = JSON.parse(bookingIdValue);
console.log(bookingId);
var servicePrice = $('#id_service_price').text().slice(1, -1);
var serviceName = $('#id_service_name').text().slice(1, -1);
console.log(serviceName, servicePrice);

const items = [{ id: serviceName, amount: servicePrice }];

let elements;

initialize();

document
    .querySelector("#payment-form")
    .addEventListener("submit", handleSubmit);

async function initialize() {
    const CSRFToken = $('input[name="csrfmiddlewaretoken"]').val();
    const response = await fetch(`/appointments/checkout/${bookingId}/`, {
        method: "POST",
        headers: { 
            "Content-Type": "application/json",
            "X-CSRFToken": CSRFToken,
        },
        
        body: JSON.stringify({ items }),
    });

    const appearance = {
        theme: 'stripe',
    };
    elements = stripe.elements({ appearance, clientSecret });

    const paymentElementOptions = {
        layout: "accordion",
    };

    const paymentElement = elements.create("payment", paymentElementOptions);
    paymentElement.mount('#payment-element');
}

async function handleSubmit(e) {
    e.preventDefault();

    const returnUrl = window.location.origin;

    const { error } = await stripe.confirmPayment({
        elements,
        confirmParams: {
            return_url: returnUrl
        },
    });
};

