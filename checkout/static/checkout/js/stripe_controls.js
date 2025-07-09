const stripe = Stripe('{{ stripe_public_key }}');
const elements = stripe.elements();
const cardElement = elements.create('card');
cardElement.mount('#card-element');

const form = document.getElementById('payment-form');
const errorMessage = document.getElementById('error-message');

// Parse JSON safely from the hidden element with id 'bag-data'
let bag = {};
try {
    bag = JSON.parse(document.getElementById('bag-data').textContent);
} catch (e) {
    errorMessage.textContent = 'Invalid bag data.';
}

const totalPrice = parseFloat(document.getElementById('total-price').textContent);

form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const { error, paymentIntent } = await stripe.confirmCardPayment(
        '{{ client_secret }}', {
        payment_method: {
            card: cardElement,
        }
    }
    );

    if (error) {
        errorMessage.textContent = error.message;
    } else if (paymentIntent.status === 'succeeded') {
        // Send order data to backend to save the order
        fetch("{% url 'save_order_data' %}", {
            method: "POST",
            headers: {
                "X-CSRFToken": "{{ csrf_token }}",
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                items: bag,
                total_price: totalPrice,
            }),
        })
            .then(res => res.json())
            .then(data => {
                if (data.status === 'success') {
                    window.location.href = `/checkout/success/${data.order_number}/`;
                } else {
                    errorMessage.textContent = 'Error saving order data.';
                }
            })
            .catch(() => {
                errorMessage.textContent = 'Network error saving order data.';
            });
    }
});
