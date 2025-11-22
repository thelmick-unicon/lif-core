/**
 * Generate a unique ID for messages
 */
export const generateId = (): string => {
  return Math.random().toString(36).substring(2, 11);
};

/**
 * Format a timestamp for display
 */
export const formatTime = (date: Date): string => {
  return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
};

/**
 * Simulate a delay (for bot responses)
 */
export const delay = (ms: number): Promise<void> => {
  return new Promise(resolve => setTimeout(resolve, ms));
};

/**
 * Calculate tokens (simplified version for demo)
 */
export const calculateTokens = (text: string): number => {
  return Math.ceil(text.split(/\s+/).length * 1.3);
};

/**
 * Calculate cost (simplified version for demo)
 */
export const calculateCost = (tokens: number): number => {
  return tokens * 0.000002; // $0.002 per 1000 tokens
};