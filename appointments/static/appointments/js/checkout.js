const stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);
const clientSecret = $('#id_client_secret').text().slice(1, -1);
const stripe = Stripe(stripePublicKey);

var servicePrice = $('#service_price').text().slice(1, -1);
var serviceName = $('#service_name').text().slice(1, -1);

const items = [{ id: serviceName, amount: servicePrice }];

let elements;

initialize();

document
    .querySelector("#payment-form")
    .addEventListener("submit", handleSubmit);

async function initialize() {
    const response = await fetch("/checkout/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ items }),
    });
    const { clientSecret } = await response.json();

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
    setLoading(true);

    const { error } = await stripe.confirmPayment({
        elements,
        confirmParams: {
            return_url: "appointments/appointments.html",
        },
    });

    if (error.type === "card_error" || error.type === "validation_error") {
        showMessage(error.message);
    } else {
        showMessage("An unexpected error occurred.");
    }

    setLoading(false);
}

