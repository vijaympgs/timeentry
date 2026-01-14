// Global TypeScript declarations
declare namespace NodeJS {
  interface Timeout {}
  interface ProcessEnv {
    NODE_ENV: 'development' | 'production' | 'test';
    // Add other environment variables as needed
  }
}

// Extend the Window interface if needed
declare global {
  interface Window {
    // Add any global window properties here
  }
}

export {}; // This file needs to be a module
