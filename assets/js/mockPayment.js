/* ==========================================================================
   mockPayment.js — Payment Gateway Simulator
   Handles QR code and Credit Card payments with simulated backend delay
   ========================================================================== */

'use strict';

const MockPayment = {
    /**
     * Process payment with hardcoded 5-second backend response delay.
     * @param {string} method - 'card' | 'qr'
     * @param {number} amount - Total amount
     * @param {object} details - Extra payment details (card info, etc.)
     * @returns {Promise<{success: boolean, transactionId: string, message: string}>}
     */
    processPayment(method, amount, details = {}) {
        return new Promise((resolve, reject) => {
            if (amount <= 0) {
                return reject(new Error('Invalid order amount.'));
            }

            if (method === 'card') {
                if (!details.cardNumber || !details.cardExpiry || !details.cardCvc) {
                    return reject(new Error('Please fill in all card details correctly.'));
                }
            }

            // Simulate 5-second backend network delay
            setTimeout(() => {
                const txId = 'TXN-' + Math.floor(100000 + Math.random() * 900000);
                resolve({
                    success: true,
                    transactionId: txId,
                    message: `Payment of $${amount.toFixed(2)} processed successfully via ${method.toUpperCase()}.`
                });
            }, 5000);
        });
    },

    /**
     * Render a simple QR Code on a canvas element
     * @param {HTMLCanvasElement} canvas 
     * @param {string} dataText 
     */
    renderQrCode(canvas, dataText) {
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        const size = 180;
        canvas.width = size;
        canvas.height = size;

        // Clear canvas
        ctx.fillStyle = '#FFFFFF';
        ctx.fillRect(0, 0, size, size);

        // Draw styled QR-like pattern matrix
        ctx.fillStyle = '#0F172A';
        const gridSize = 10;
        const cellSize = size / gridSize;

        for (let r = 0; r < gridSize; r++) {
            for (let c = 0; c < gridSize; c++) {
                // Corner positioning squares
                const isTopLeftCorner = (r < 3 && c < 3);
                const isTopRightCorner = (r < 3 && c >= gridSize - 3);
                const isBottomLeftCorner = (r >= gridSize - 3 && c < 3);

                if (isTopLeftCorner || isTopRightCorner || isBottomLeftCorner) {
                    if (r === 1 && c === 1) continue;
                    if (r === 1 && c === gridSize - 2) continue;
                    if (r === gridSize - 2 && c === 1) continue;
                    ctx.fillRect(c * cellSize, r * cellSize, cellSize, cellSize);
                } else if ((r + c + (dataText ? dataText.length : 5)) % 2 === 0) {
                    ctx.fillRect(c * cellSize + 1, r * cellSize + 1, cellSize - 2, cellSize - 2);
                }
            }
        }
    }
};

window.MockPayment = MockPayment;
