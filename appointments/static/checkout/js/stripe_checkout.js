const clientSecret = $('#id_client_secret').text().slice(1, -1);
const stripe = Stripe(clientSecret);

initialize();

// fetches Checkout session and retrieves the client secret
async function initialize() {
    const fetchClientSecret = async () => {
        const response = await fetch("/add_appointment/<int:service_id>", {
            method: "POST",
        });
        const { clientSecret } = await response.json();
        return clientSecret;
    };

    // Initialise checkout
    const checkout = await stripe.initEmbeddedCheckout({
        fetchClientSecret,
    });

    // Mount checkout
    checkout.mount('#checkout');
};