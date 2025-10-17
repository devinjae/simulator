function PlaceholderBox({ title }: { title: string }) {
  return (
    <div className="placeholder">
      <strong>{title}</strong>
      <div style={{ marginTop: 8, color: '#666' }}>Empty</div>
    </div>
  )
}

function TradesPage() {
  return (
    <div className="trades">
      <aside className="trades-aside">
        <h3 style={{ marginTop: 0 }}>Widgets</h3>
        <ul style={{ listStyle: 'none', padding: 0, margin: 0, display: 'grid', gap: 8 }}>
          <li>Leaderboard</li>
          <li>Portfolio</li>
          <li>News Feed</li>
          <li>Stocks</li>
          <li>Order Book</li>
          <li>Buy/Sell Widget</li>
        </ul>
      </aside>
      <main className="trades-main">
        <div className="widget-grid">
          <PlaceholderBox title="Leaderboard" />
          <PlaceholderBox title="Portfolio" />
          <PlaceholderBox title="News Feed" />
          <PlaceholderBox title="Stocks" />
          <PlaceholderBox title="Order Book" />
          <PlaceholderBox title="Buy/Sell" />
        </div>
      </main>
    </div>
  )
}

export default TradesPage


