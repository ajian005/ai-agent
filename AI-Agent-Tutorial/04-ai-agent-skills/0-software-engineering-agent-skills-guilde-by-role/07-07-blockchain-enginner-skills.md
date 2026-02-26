# Blockchain Engineer Skills

The Blockchain Engineer specializes in developing decentralized applications (dApps) and smart contracts using blockchain technology.

## Role Definition
Focuses on cryptography, consensus mechanisms, smart contract development, and web3 integration.

## Skills & Tools

### 1. Smart Contract Development
Writing code that runs on the blockchain.

- **Tool: Solidity**
  - *Description*: The primary language for Ethereum smart contracts.
  - *Practice*: Write secure contracts for tokens (ERC-20, ERC-721) and logic.
  - *Agent Prompt*: "Write an ERC-20 token contract with a minting function."

- **Tool: Rust / Ink!**
  - *Description*: For ecosystems like Polkadot/Substrate or Solana.
  - *Practice*: Write high-performance contracts.
  - *Agent Prompt*: "Explain the ownership model in Rust for Solana programs."

### 2. Development Frameworks
Building and testing dApps.

- **Tool: Hardhat / Foundry**
  - *Description*: Development environments for Ethereum.
  - *Practice*: Compile, deploy, test, and debug contracts.
  - *Agent Prompt*: "Write a Hardhat script to deploy a contract to the Goerli testnet."

- **Tool: Ganache / Anvil**
  - *Description*: Local blockchain for development.
  - *Practice*: Simulate a blockchain locally for fast iteration.
  - *Agent Prompt*: "Start a local Ganache instance and deploy a contract."

### 3. Web3 Integration (Frontend)
Connecting the user to the blockchain.

- **Tool: Ethers.js / Viem**
  - *Description*: JavaScript libraries for interacting with the Ethereum blockchain.
  - *Practice*: Connect wallets (MetaMask), query state, and send transactions.
  - *Agent Prompt*: "Use Ethers.js to connect to a wallet and get the current balance."

- **Tool: The Graph**
  - *Description*: Indexing protocol for querying networks.
  - *Practice*: Build subgraphs to query blockchain data efficiently via GraphQL.
  - *Agent Prompt*: "Define a subgraph schema for indexing token transfers."

### 4. Security & Cryptography
Ensuring the system is trustless and secure.

- **Tool: Smart Contract Auditing**
  - *Description*: Identifying vulnerabilities (Reentrancy, Overflow).
  - *Practice*: Use tools like Slither or Mythril.
  - *Agent Prompt*: "Explain the Reentrancy attack and how to prevent it."

- **Tool: Cryptographic Primitives**
  - *Description*: Hashing (Keccak-256), Digital Signatures (ECDSA).
  - *Practice*: Understand how keys and addresses are generated.
  - *Agent Prompt*: "Explain how an Ethereum address is derived from a public key."
