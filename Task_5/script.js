const commandInput = document.getElementById('commandInput');
const outputDiv = document.getElementById('output');
const productsDiv = document.getElementById('products');

commandInput.addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        const command = commandInput.value;
        handleCommand(command);
        commandInput.value = '';
    }
});

function printToTerminal(text) {
    const p = document.createElement('p');
    p.textContent = text;
    outputDiv.appendChild(p);
    outputDiv.scrollTop = outputDiv.scrollHeight;
}

function displayProducts(products) {
    productsDiv.innerHTML = ''; // Clear existing products
    products.forEach(product => {
        const productDiv = document.createElement('div');
        productDiv.className = 'product';
        productDiv.innerHTML = `
            <img src="${product.image}" alt="${product.title}">
            <h3>${product.title}</h3>
            <p>$${product.price}</p>
        `;
        productsDiv.appendChild(productDiv);
    });
}

function fetchAllProducts() {
    fetch('https://fakestoreapi.com/products')
        .then(response => response.json())
        .then(data => {
            displayProducts(data);
        })
        .catch(error => console.error('Error:', error));
}

function fetchProductDetails(productId) {
    fetch(`https://fakestoreapi.com/products/${productId}`)
        .then(response => response.json())
        .then(product => {
            printToTerminal(`ID: ${product.id} | ${product.title} | $${product.price}`);
            printToTerminal(`Description: ${product.description}`);
        })
        .catch(error => console.error('Error:', error));
}

function handleCommand(command) {
    const args = command.split(' ');
    const cmd = args[0];
    const param = args[1];

    switch(cmd) {
        case 'list':
            fetchAllProducts();
            break;
        case 'details':
            fetchProductDetails(param);
            break;
        case 'clear':
            outputDiv.innerHTML = '';
            break;
        default:
            printToTerminal(`Unknown command: ${cmd}`);
    }
}

