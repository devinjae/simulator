interface LatencyPillProps {
  latencyMs: number | null
  isConnected: boolean
  isReconnecting: boolean
}

function LatencyPill({ latencyMs, isConnected, isReconnecting }: LatencyPillProps) {
  const getStatus = () => {
    if (isReconnecting) {
      return { text: 'Reconnecting...', color: '#f59e0b', bgColor: '#fef3c7' }
    }
    if (!isConnected) {
      return { text: 'Disconnected', color: '#dc2626', bgColor: '#fee2e2' }
    }
    if (latencyMs === null) {
      return { text: 'Connecting...', color: '#6b7280', bgColor: '#f3f4f6' }
    }
    if (latencyMs > 500) {
      return { text: `${latencyMs}ms (degraded)`, color: '#f59e0b', bgColor: '#fef3c7' }
    }
    return { text: `${latencyMs}ms`, color: '#10b981', bgColor: '#d1fae5' }
  }

  const status = getStatus()

  return (
    <div
      style={{
        display: 'inline-flex',
        alignItems: 'center',
        gap: 6,
        padding: '4px 10px',
        borderRadius: 12,
        fontSize: 13,
        fontWeight: 500,
        color: status.color,
        backgroundColor: status.bgColor,
        transition: 'all 0.2s ease',
      }}
    >
      <div
        style={{
          width: 6,
          height: 6,
          borderRadius: '50%',
          backgroundColor: status.color,
          animation: isConnected && !isReconnecting ? 'pulse 2s ease-in-out infinite' : 'none',
        }}
      />
      <span>{status.text}</span>
      <style>{`
        @keyframes pulse {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.5; }
        }
      `}</style>
    </div>
  )
}

export default LatencyPill
