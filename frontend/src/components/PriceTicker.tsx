import React from 'react';
import { useWebSocketContext } from '../contexts/WebSocketContext';

const PriceTicker: React.FC = () => {
  const { prices, lastUpdated, isConnected } = useWebSocketContext();

  return (
    <div className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-lg font-semibold text-gray-900 dark:text-white">
          Live Prices
        </h2>
        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
          isConnected 
            ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
            : 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200'
        }`}>
          {isConnected ? 'Connected' : 'Disconnected'}
        </span>
      </div>
      
      <div className="space-y-2 max-h-60 overflow-y-auto">
        {Object.entries(prices).length > 0 ? (
          Object.entries(prices).map(([ticker, price]) => (
            <div key={ticker} className="flex justify-between items-center py-1">
              <span className="font-medium text-gray-700 dark:text-gray-300">{ticker}: </span>
              <span className="font-mono text-green-600 dark:text-green-400">
                ${price.toFixed(2)}
              </span>
            </div>
          ))
        ) : (
          <div className="text-center py-4 text-gray-500 dark:text-gray-400">
            {isConnected ? 'Waiting for price updates...' : 'Connecting to price feed...'}
          </div>
        )}
      </div>
      
      {lastUpdated && (
        <div className="mt-3 pt-2 border-t border-gray-200 dark:border-gray-700 text-xs text-gray-500 dark:text-gray-400">
          Last updated: {new Date(lastUpdated).toLocaleTimeString()} lmao
        </div>
      )}
    </div>
  );
};

export default PriceTicker;