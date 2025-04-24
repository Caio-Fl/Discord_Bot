import streamlit as st
import streamlit.components.v1 as components

st.title("🦊 Connect MetaMask Wallet")

# JavaScript for MetaMask connection
components.html("""
    <script>
        async function connectWallet() {
            if (window.ethereum) {
                try {
                    const accounts = await ethereum.request({ method: 'eth_requestAccounts' });
                    const walletAddress = accounts[0];
                    document.getElementById("wallet-address").innerText = walletAddress;
                    window.parent.postMessage({type: 'WALLET_ADDRESS', wallet: walletAddress}, '*');
                } catch (err) {
                    alert("Connection error: " + err.message);
                }
            } else {
                alert("MetaMask not detected.");
            }
        }
    </script>

    <button onclick="connectWallet()">🔌 Connect Wallet</button>
    <p>Connected Wallet: <span id="wallet-address">Not connected</span></p>
""", height=150)