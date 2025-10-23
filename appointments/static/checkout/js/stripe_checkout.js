const stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);
const stripe = Stripe(stripePublicKey);
const clientSecret = $('#id_client_secret');
const form = document.getElementById('booking-form');

form.addEventListener('submit', async function(e) {
    e.preventDefault();

    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());
    const serviceId = $('#service_id').val();
    const csrfToken = $('input[name="csrfmiddlewaretoken"]').val();

    console.log("Client-side 'data' object:", data);

    try {
        const response = await fetch(`/appointments/checkout/create/${serviceId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify({ form_data: data })
        });
        if (!response.ok) {
            const errorData = await response.json();
            console.error('Server-side validation failed:', errorData);
            return;
        }       

        const checkout = await stripe.initEmbeddedCheckout({
            clientSecret,
        });

        checkout.mount('#checkout');

        form.style.display = 'none';
        document.getElementById('checkout-container').style.display = 'block';
    } catch (error) {
        console.log('An error occured:', error);
    }
});