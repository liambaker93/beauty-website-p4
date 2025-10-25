const stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);
const stripe = Stripe(stripePublicKey);

const bookingIdElement = document.getElementById('id_appointment_id');
const bookingIdValue = bookingIdElement.textContent;
const bookingId = JSON.parse(bookingIdValue);
console.log(bookingId);

let elements;

initialize();

document
    .querySelector("#payment-form")
    .addEventListener("submit", handleSubmit);

async function initialize() {
    const CSRFToken = $('input[name="csrfmiddlewaretoken"]').val();
    const response = await fetch(`/appointments/checkout_intent/${bookingId}/`, {
        method: "POST",
        headers: { 
            "Content-Type": "application/json",
            "X-CSRFToken": CSRFToken,
        },
        
        body: JSON.stringify({ booking_id: bookingId }),
    });

    if (!response.ok) {
        console.error("Failed to create payment intent on server.");
        return;
    }    

    const { clientSecret: freshClientSecret } = await response.json();

    const appearance = {
        theme: 'stripe',
    };
    elements = stripe.elements({ appearance, clientSecret: freshClientSecret });

    const paymentElementOptions = {
        layout: "accordion",
    };

    const paymentElement = elements.create("payment", paymentElementOptions);
    paymentElement.mount('#payment-element');
}

async function handleSubmit(e) {
    e.preventDefault();

    const returnUrl = window.location.origin + '/appointments/booking_confirmed/';

    const { error } = await stripe.confirmPayment({
        elements,
        confirmParams: {
            return_url: returnUrl
        },
    });

    if (error.type === "card_error" || error.type === "validation_error") {
        console.error(error.message);
    } else {
        console.error("An unexpected error occured.", error);
    }
};

