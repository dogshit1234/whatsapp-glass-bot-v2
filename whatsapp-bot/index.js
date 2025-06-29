const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const axios = require('axios');
require('dotenv').config();
const BACKEND_API_URL = process.env.BACKEND_API_URL || 'http://localhost:5000';

const client = new Client({
    authStrategy: new LocalAuth(),
    puppeteer: {
        headless: true,
        args: [
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-dev-shm-usage',
            '--disable-accelerated-2d-canvas',
            '--no-first-run',
            '--no-zygote',
            '--single-process',
            '--disable-gpu'
        ]
    }
});

client.on('qr', qr => {
    qrcode.generate(qr, { small: true });
    console.log('Scan this QR with your WhatsApp Business app.');
});

client.on('ready', () => {
    console.log('WhatsApp bot is ready!');
});

// Welcome message with available commands
const welcomeMessage = `🤖 *Welcome to WhatsApp Glass Bot!*

I can help you manage your glass orders. Here are the available commands:

📋 *View Orders:*
• \`/pending\` - Show all pending orders
• \`/ready\` - Show all ready orders  
• \`/delivered\` - Show all delivered orders
• \`/completed\` - Show all completed orders
• \`/all\` - Show summary of all tabs

🔍 *Search & Status:*
• \`/search [term]\` - Search orders by ID, client name, or specs
• \`/status [client/ID]\` - Find specific order status

🔄 *Update Orders:*
• \`/update [order_id] [status]\` - Update order status

📝 *Add New Order:*
Just send your order details as text!

Type \`/help\` for detailed help anytime.`;

client.on('message', async msg => {
    console.log('=== NEW MESSAGE RECEIVED ===');
    console.log('From:', msg.from);
    console.log('Body:', msg.body);
    console.log('Message Type:', msg.type);
    console.log('================================');
    
    // Handle media messages by asking for text input instead
    if (msg.hasMedia) {
        console.log('=== MEDIA MESSAGE RECEIVED - REDIRECTING TO TEXT ===');
        await client.sendMessage(msg.from, 
            '📝 Please send your order details as text instead of an image.\n\n' +
            'For example:\n' +
            'Client Name: John Doe\n' +
            'Glass Specifications: 10mm Clear Glass\n' +
            'Sizes: 2000x1000\n' +
            'Quantity: 2\n' +
            'Notes: Tempered glass'
        );
        return;
    }
    
    // Process text messages (commands or orders)
    if (msg.body && msg.body.trim()) {
        try {
            console.log('=== PROCESSING TEXT MESSAGE ===');
            const response = await axios.post(`${BACKEND_API_URL}/api/whatsapp_in`, {
                from: msg.from,
                body: msg.body,
                hasMedia: false
            });
            
            if (response.data.reply) {
                await client.sendMessage(msg.from, response.data.reply);
                console.log('Reply sent successfully');
            }
        } catch (e) {
            console.error('Text processing error:', e.message);
            await client.sendMessage(msg.from, '❌ Error processing your request. Please try again or contact support.');
        }
    } else {
        // Empty message - send welcome message
        await client.sendMessage(msg.from, welcomeMessage);
    }
});

client.initialize(); 