import PriceChart from "../components/chart"

function TradesPage() {
  return (
    <div className="trades">
      <aside className="overlay-aside">
        <h3 className="overlay-title">Widgets</h3>
        <ul className="widgets-list">
          <li>Leaderboard</li>
          <li>Portfolio</li>
          <li>News Feed</li>
          <li>Stocks</li>
          <li>Orderbook</li>
          <li>Buy/Sell Widget</li>
        </ul>
      </aside>
      
      <PriceChart />
      <div className="trades-stage" />
    </div>
  )
}

export default TradesPage


