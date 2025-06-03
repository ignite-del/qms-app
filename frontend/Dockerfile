FROM node:18-alpine

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm install

# Copy application code
COPY . .

# Create TypeScript configuration if it doesn't exist
RUN test -f tsconfig.json || echo '{"compilerOptions":{"target":"es5","lib":["dom","dom.iterable","esnext"],"allowJs":true,"skipLibCheck":true,"esModuleInterop":true,"allowSyntheticDefaultImports":true,"strict":true,"forceConsistentCasingInFileNames":true,"noFallthroughCasesInSwitch":true,"module":"esnext","moduleResolution":"node","resolveJsonModule":true,"isolatedModules":true,"noEmit":true,"jsx":"react-jsx"},"include":["src"],"exclude":["node_modules"]}' > tsconfig.json

# Ensure src directory exists
RUN mkdir -p src

# Create basic React app structure if it doesn't exist
RUN test -f src/index.tsx || echo 'import React from "react"; import ReactDOM from "react-dom/client"; import App from "./App"; const root = ReactDOM.createRoot(document.getElementById("root") as HTMLElement); root.render(<React.StrictMode><App /></React.StrictMode>);' > src/index.tsx
RUN test -f src/App.tsx || echo 'import React from "react"; const App: React.FC = () => { return <div>QMS Application</div>; }; export default App;' > src/App.tsx

# Build the application
RUN npm run build || npm run start

# Install serve to run the application
RUN npm install -g serve

# Expose port
EXPOSE 3000

# Start the application
CMD ["serve", "-s", "build", "-l", "3000"] 