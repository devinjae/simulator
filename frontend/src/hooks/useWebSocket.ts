import { useEffect, useRef, useState, useCallback } from 'react'

interface UseWebSocketOptions {
  url: string
  onMessage?: (data: any) => void
  onError?: (error: Event) => void
  pingInterval?: number // ms between pings
  maxRetries?: number
  initialBackoff?: number // ms
  maxBackoff?: number // ms
}

interface WebSocketState {
  isConnected: boolean
  latencyMs: number | null
  lastPongAt: number | null
  retryCount: number
  isReconnecting: boolean
}

export function useWebSocket({
  url,
  onMessage,
  onError,
  pingInterval = 5000,
  maxRetries = 10,
  initialBackoff = 500,
  maxBackoff = 10000,
}: UseWebSocketOptions) {
  const [state, setState] = useState<WebSocketState>({
    isConnected: false,
    latencyMs: null,
    lastPongAt: null,
    retryCount: 0,
    isReconnecting: false,
  })

  const wsRef = useRef<WebSocket | null>(null)

  // avoid node js issue
  const pingTimerRef = useRef<ReturnType<typeof setInterval> | null>(null)
  const reconnectTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null)
  const pingTimestampRef = useRef<number | null>(null)
  const retryCountRef = useRef(0)

  const clearTimers = useCallback(() => {
    if (pingTimerRef.current) {
      clearInterval(pingTimerRef.current)
      pingTimerRef.current = null
    }
    if (reconnectTimerRef.current) {
      clearTimeout(reconnectTimerRef.current)
      reconnectTimerRef.current = null
    }
  }, [])

  const calculateBackoff = useCallback((retryCount: number) => {
    // Exponential backoff with jitter
    const exponentialBackoff = Math.min(initialBackoff * Math.pow(2, retryCount), maxBackoff)
    const jitter = Math.random() * 0.3 * exponentialBackoff // ±30% jitter
    return exponentialBackoff + jitter
  }, [initialBackoff, maxBackoff])

  const startPingPong = useCallback(() => {
    if (pingTimerRef.current) {
      clearInterval(pingTimerRef.current)
    }

    pingTimerRef.current = setInterval(() => {
      if (wsRef.current?.readyState === WebSocket.OPEN) {
        pingTimestampRef.current = Date.now()
        wsRef.current.send('ping')
      }
    }, pingInterval)
  }, [pingInterval])

  const connect = useCallback(() => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      return
    }

    try {
      const ws = new WebSocket(url)
      wsRef.current = ws

      ws.onopen = () => {
        console.log('WebSocket connected')
        setState(prev => ({
          ...prev,
          isConnected: true,
          isReconnecting: false,
        }))
        retryCountRef.current = 0
        startPingPong()
      }

      ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data)
          
          // Handle pong response
          if (data.type === 'pong' && pingTimestampRef.current) {
            const rtt = Date.now() - pingTimestampRef.current
            setState(prev => ({
              ...prev,
              latencyMs: rtt,
              lastPongAt: Date.now(),
            }))
            pingTimestampRef.current = null
          } else {
            // Regular message
            onMessage?.(data)
          }
        } catch (err) {
          // Not JSON, treat as regular message
          onMessage?.(event.data)
        }
      }

      ws.onerror = (error) => {
        console.error('WebSocket error:', error)
        onError?.(error)
      }

      ws.onclose = () => {
        console.log('WebSocket closed')
        setState(prev => ({ ...prev, isConnected: false }))
        clearTimers()

        // Attempt reconnection with backoff
        if (retryCountRef.current < maxRetries) {
          const backoffMs = calculateBackoff(retryCountRef.current)
          console.log(`Reconnecting in ${Math.round(backoffMs)}ms (attempt ${retryCountRef.current + 1}/${maxRetries})`)
          
          setState(prev => ({
            ...prev,
            isReconnecting: true,
            retryCount: retryCountRef.current + 1,
          }))

          reconnectTimerRef.current = setTimeout(() => {
            retryCountRef.current++
            connect()
          }, backoffMs)
        } else {
          console.error('Max reconnection attempts reached')
          setState(prev => ({
            ...prev,
            isReconnecting: false,
          }))
        }
      }
    } catch (err) {
      console.error('Failed to create WebSocket:', err)
    }
  }, [url, onMessage, onError, startPingPong, clearTimers, calculateBackoff, maxRetries])

  const disconnect = useCallback(() => {
    clearTimers()
    if (wsRef.current) {
      wsRef.current.close()
      wsRef.current = null
    }
  }, [clearTimers])

  const send = useCallback((data: any) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(typeof data === 'string' ? data : JSON.stringify(data))
    } else {
      console.warn('WebSocket is not connected')
    }
  }, [])

  useEffect(() => {
    connect()
    return () => {
      disconnect()
    }
  }, [connect, disconnect])

  return {
    ...state,
    send,
    reconnect: connect,
    disconnect,
  }
}
