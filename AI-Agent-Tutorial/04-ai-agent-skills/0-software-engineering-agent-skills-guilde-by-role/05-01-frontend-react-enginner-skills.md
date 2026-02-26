# Frontend React Engineer Skills

The Frontend React Engineer specializes in building user interfaces using the React library. They focus on component architecture, state management, and performance.

## Role Definition
Focuses on component reusability, hooks, state management patterns, and the React ecosystem.

## Skills & Tools

### 1. Component Architecture
Building scalable and maintainable UI components.

- **Tool: Functional Components & Hooks**
  - *Description*: Modern React patterns.
  - *Practice*: Use `useState`, `useEffect`, `useContext`, and custom hooks.
  - *Agent Prompt*: "Refactor this Class component to a Functional component with Hooks."

- **Tool: Component Composition**
  - *Description*: Building complex UIs from smaller, isolated pieces.
  - *Practice*: Use `children` prop and render props pattern.
  - *Agent Prompt*: "Design a 'Card' component that accepts arbitrary content via children."

### 2. State Management
Handling data flow across the application.

- **Tool: Redux Toolkit (RTK)**
  - *Description*: Standard way to write Redux logic.
  - *Practice*: Define slices, reducers, and async thunks.
  - *Agent Prompt*: "Create a Redux slice for managing user authentication state."

- **Tool: React Context API**
  - *Description*: Sharing global data without prop drilling.
  - *Practice*: Use for theme, language, or user settings.
  - *Agent Prompt*: "Implement a ThemeProvider using React Context."

- **Tool: React Query / TanStack Query**
  - *Description*: Managing server state (fetching, caching, updating).
  - *Practice*: Replace `useEffect` fetching with `useQuery`.
  - *Agent Prompt*: "Refactor this data fetching logic to use React Query."

### 3. Performance Optimization
Ensuring the app is fast and responsive.

- **Tool: React.memo & useMemo**
  - *Description*: Memoization to prevent unnecessary re-renders.
  - *Practice*: Profile components and optimize expensive calculations.
  - *Agent Prompt*: "Analyze why this list component is re-rendering too often."

- **Tool: Code Splitting (React.lazy)**
  - *Description*: Loading code only when needed.
  - *Practice*: Implement route-based code splitting.
  - *Agent Prompt*: "Implement lazy loading for the 'Admin Dashboard' route."

### 4. Testing React Apps
Verifying component behavior.

- **Tool: React Testing Library (RTL)**
  - *Description*: Testing components from the user's perspective.
  - *Practice*: Test user interactions (clicks, inputs) and assertions.
  - *Agent Prompt*: "Write a test to verify the form submits when the button is clicked."

- **Tool: Vitest**
  - *Description*: Fast unit test runner.
  - *Practice*: Run tests in a simulated browser environment.
  - *Agent Prompt*: "Configure Vitest for a Vite-based React project."
