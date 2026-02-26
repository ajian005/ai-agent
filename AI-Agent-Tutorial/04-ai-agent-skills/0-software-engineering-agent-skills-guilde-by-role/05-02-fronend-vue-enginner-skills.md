# Frontend Vue Engineer Skills

The Frontend Vue Engineer specializes in building user interfaces using the Vue.js framework. They focus on reactivity, component composition, and the Vue ecosystem.

## Role Definition
Focuses on the Options/Composition API, state management with Pinia/Vuex, and directive-based templating.

## Skills & Tools

### 1. Vue.js Core
Mastering the framework.

- **Tool: Composition API**
  - *Description*: A set of additive, function-based APIs that allow flexible composition of component logic.
  - *Practice*: Use `ref`, `reactive`, and `computed` to manage state.
  - *Agent Prompt*: "Refactor this Options API component to use Script Setup and Composition API."

- **Tool: Directives**
  - *Description*: Special attributes in markup (v-if, v-for, v-model).
  - *Practice*: Build dynamic templates efficiently.
  - *Agent Prompt*: "Create a custom directive `v-focus` that focuses the input element on mount."

### 2. State Management
Handling global application state.

- **Tool: Pinia**
  - *Description*: The intuitive, type-safe store for Vue.
  - *Practice*: Define stores, getters, and actions.
  - *Agent Prompt*: "Create a Pinia store for managing the user's shopping cart."

- **Tool: Vuex (Legacy)**
  - *Description*: State management pattern + library for Vue.js applications.
  - *Practice*: Maintain legacy codebases with mutations and actions.
  - *Agent Prompt*: "Explain how to migrate a Vuex module to Pinia."

### 3. Routing & Meta Frameworks
Navigating the app.

- **Tool: Vue Router**
  - *Description*: The official router for Vue.js.
  - *Practice*: Configure nested routes, guards, and lazy loading.
  - *Agent Prompt*: "Set up a navigation guard to protect the `/admin` route."

- **Tool: Nuxt.js**
  - *Description*: The intuitive Vue framework for SSR and SSG.
  - *Practice*: Build SEO-friendly universal applications.
  - *Agent Prompt*: "Create a Nuxt page with async data fetching using `useFetch`."

### 4. Testing & Tooling
Ensuring quality.

- **Tool: Vue Test Utils**
  - *Description*: The official unit testing utility library for Vue.js.
  - *Practice*: Mount components and trigger events.
  - *Agent Prompt*: "Write a unit test to verify the component emits an event on click."

- **Tool: Vite**
  - *Description*: Next Generation Frontend Tooling.
  - *Practice*: Optimize build configuration and plugins.
  - *Agent Prompt*: "Configure Vite to use a proxy for API requests in development."
