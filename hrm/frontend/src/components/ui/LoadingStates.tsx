import React from 'react';
import { RefreshCw, AlertCircle, CheckCircle, XCircle, Wifi, WifiOff } from 'lucide-react';

// Loading spinner component
export const LoadingSpinner: React.FC<{
  size?: 'sm' | 'md' | 'lg';
  className?: string;
}> = ({ size = 'md', className = '' }) => {
  const sizeClasses = {
    sm: 'w-4 h-4',
    md: 'w-6 h-6',
    lg: 'w-8 h-8'
  };

  return (
    <div className={`animate-spin ${sizeClasses[size]} ${className}`}>
      <RefreshCw className="w-full h-full text-blue-600" />
    </div>
  );
};

// Full page loading state
export const FullPageLoading: React.FC<{
  message?: string;
}> = ({ message = 'Loading...' }) => {
  return (
    <div className="flex flex-col items-center justify-center h-64">
      <LoadingSpinner size="lg" />
      <p className="mt-4 text-gray-600">{message}</p>
    </div>
  );
};

// Inline loading state for buttons
export const ButtonLoading: React.FC<{
  text?: string;
}> = ({ text = 'Loading...' }) => {
  return (
    <div className="flex items-center space-x-2">
      <LoadingSpinner size="sm" />
      <span>{text}</span>
    </div>
  );
};

// Error state component
export const ErrorState: React.FC<{
  title?: string;
  message: string;
  onRetry?: () => void;
  retryText?: string;
}> = ({ 
  title = 'Error', 
  message, 
  onRetry, 
  retryText = 'Try Again' 
}) => {
  return (
    <div className="flex flex-col items-center justify-center p-6 bg-red-50 border border-red-200 rounded-lg">
      <XCircle className="w-12 h-12 text-red-600 mb-4" />
      <h3 className="text-lg font-semibold text-red-900 mb-2">{title}</h3>
      <p className="text-red-700 text-center mb-4">{message}</p>
      {onRetry && (
        <button
          onClick={onRetry}
          className="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 transition-colors duration-200"
        >
          {retryText}
        </button>
      )}
    </div>
  );
};

// Success state component
export const SuccessState: React.FC<{
  title?: string;
  message: string;
  onDismiss?: () => void;
}> = ({ 
  title = 'Success', 
  message, 
  onDismiss 
}) => {
  return (
    <div className="flex flex-col items-center justify-center p-6 bg-green-50 border border-green-200 rounded-lg">
      <CheckCircle className="w-12 h-12 text-green-600 mb-4" />
      <h3 className="text-lg font-semibold text-green-900 mb-2">{title}</h3>
      <p className="text-green-700 text-center mb-4">{message}</p>
      {onDismiss && (
        <button
          onClick={onDismiss}
          className="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 transition-colors duration-200"
        >
          Dismiss
        </button>
      )}
    </div>
  );
};

// Empty state component
export const EmptyState: React.FC<{
  title?: string;
  message: string;
  action?: {
    text: string;
    onClick: () => void;
  };
  icon?: React.ReactNode;
}> = ({ 
  title = 'No Data', 
  message, 
  action,
  icon 
}) => {
  const defaultIcon = <AlertCircle className="w-12 h-12 text-gray-400" />;
  
  return (
    <div className="flex flex-col items-center justify-center p-8 text-center">
      {icon || defaultIcon}
      <h3 className="text-lg font-semibold text-gray-900 mb-2">{title}</h3>
      <p className="text-gray-600 mb-6 max-w-md">{message}</p>
      {action && (
        <button
          onClick={action.onClick}
          className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors duration-200"
        >
          {action.text}
        </button>
      )}
    </div>
  );
};

// Connection status indicator
export const ConnectionStatus: React.FC<{
  isOnline: boolean;
  isConnecting?: boolean;
}> = ({ isOnline, isConnecting = false }) => {
  if (isConnecting) {
    return (
      <div className="flex items-center space-x-2 text-yellow-600">
        <LoadingSpinner size="sm" />
        <span className="text-sm">Connecting...</span>
      </div>
    );
  }

  return (
    <div className={`flex items-center space-x-2 ${isOnline ? 'text-green-600' : 'text-red-600'}`}>
      {isOnline ? (
        <Wifi className="w-4 h-4" />
      ) : (
        <WifiOff className="w-4 h-4" />
      )}
      <span className="text-sm">{isOnline ? 'Online' : 'Offline'}</span>
    </div>
  );
};

// Data table loading skeleton
export const TableSkeleton: React.FC<{
  rows?: number;
  columns?: number;
}> = ({ rows = 5, columns = 4 }) => {
  return (
    <div className="overflow-x-auto">
      <table className="min-w-full divide-y divide-gray-200">
        <thead className="bg-gray-50">
          <tr>
            {Array.from({ length: columns }).map((_, index) => (
              <th key={index} className="px-6 py-3 text-left">
                <div className="h-4 bg-gray-200 rounded animate-pulse"></div>
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          {Array.from({ length: rows }).map((_, rowIndex) => (
            <tr key={rowIndex}>
              {Array.from({ length: columns }).map((_, colIndex) => (
                <td key={colIndex} className="px-6 py-4 whitespace-nowrap">
                  <div className="h-4 bg-gray-200 rounded animate-pulse"></div>
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

// Card loading skeleton
export const CardSkeleton: React.FC<{
  lines?: number;
}> = ({ lines = 3 }) => {
  return (
    <div className="p-6 bg-white rounded-lg shadow">
      <div className="h-6 bg-gray-200 rounded animate-pulse mb-4"></div>
      {Array.from({ length: lines }).map((_, index) => (
        <div key={index} className="h-4 bg-gray-200 rounded animate-pulse mb-2"></div>
      ))}
    </div>
  );
};

// Hook for managing loading states
export const useLoadingState = () => {
  const [isLoading, setIsLoading] = React.useState(false);
  const [error, setError] = React.useState<string | null>(null);
  const [success, setSuccess] = React.useState<string | null>(null);

  const execute = async <T,>(
    operation: () => Promise<T>,
    options?: {
      successMessage?: string;
      errorMessage?: string;
    }
  ): Promise<T | null> => {
    try {
      setIsLoading(true);
      setError(null);
      setSuccess(null);
      
      const result = await operation();
      
      if (options?.successMessage) {
        setSuccess(options.successMessage);
      }
      
      return result;
    } catch (err) {
      const errorMessage = options?.errorMessage || 
        (err instanceof Error ? err.message : 'An error occurred');
      setError(errorMessage);
      return null;
    } finally {
      setIsLoading(false);
    }
  };

  const reset = () => {
    setIsLoading(false);
    setError(null);
    setSuccess(null);
  };

  return {
    isLoading,
    error,
    success,
    execute,
    reset,
    setIsLoading,
    setError,
    setSuccess
  };
};
