import './App.css'
import BalanceReportForm from './components/BalanceReportForm'
import DateRangeProcessor from './components/DateRangeProcessor'

function App() {
  return (
    <div className="App">
      <header className="app-header">
        <h1>Siigo - Reportes y Consultas</h1>
        <p>Sistema de integración con la API de Siigo</p>
      </header>

      <main className="app-main">
        <DateRangeProcessor />
        <div style={{ marginTop: '3rem' }}>
          <BalanceReportForm />
        </div>
      </main>

      <footer className="app-footer">
        <p>Versión 1.0.0 - Powered by Siigo API</p>
      </footer>
    </div>
  )
}

export default App
