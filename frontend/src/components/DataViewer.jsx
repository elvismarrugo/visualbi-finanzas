import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './DataViewer.css';

const DataViewer = () => {
  const [stats, setStats] = useState(null);
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [filters, setFilters] = useState({
    año: '',
    periodo: '',
    limit: 10
  });

  // Cargar estadísticas al montar el componente
  useEffect(() => {
    loadStats();
  }, []);

  const loadStats = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/powerbi/stats', {
        timeout: 10000 // 10 segundos de timeout
      });
      setStats(response.data);
    } catch (err) {
      console.error('Error cargando estadísticas:', err);
      if (err.code === 'ECONNREFUSED' || err.message.includes('Network Error')) {
        setError('No se pudo conectar con el backend. Verifica que esté corriendo en http://localhost:8000');
      }
    }
  };

  const loadData = async () => {
    setLoading(true);
    setError(null);
    setData(null);

    try {
      const params = new URLSearchParams();
      if (filters.año) params.append('año', filters.año);
      if (filters.periodo) params.append('periodo', filters.periodo);
      params.append('limit', filters.limit);

      const response = await axios.get(
        `http://localhost:8000/api/powerbi/balance-reports?${params.toString()}`
      );
      setData(response.data);
    } catch (err) {
      if (err.response) {
        setError(`Error: ${err.response.data.detail || 'Error desconocido'}`);
      } else if (err.request) {
        setError('Error: No se pudo conectar con el servidor.');
      } else {
        setError(`Error: ${err.message}`);
      }
    } finally {
      setLoading(false);
    }
  };

  const handleFilterChange = (e) => {
    const { name, value } = e.target;
    setFilters(prev => ({
      ...prev,
      [name]: value
    }));
  };

  return (
    <div className="data-viewer">
      <div className="viewer-header">
        <h2>📊 Ver Datos Procesados</h2>
        <button onClick={loadStats} className="refresh-button">
          🔄 Actualizar Estadísticas
        </button>
      </div>

      {/* Estadísticas */}
      {stats && (
        <div className="stats-container">
          <h3>📈 Estadísticas</h3>
          <div className="stats-grid">
            <div className="stat-item">
              <strong>Total de Registros:</strong>
              <span className="stat-value">{stats.total_records.toLocaleString()}</span>
            </div>
            <div className="stat-item">
              <strong>Saldo Final Total:</strong>
              <span className="stat-value">
                ${stats.total_saldo_final.toLocaleString('es-ES', { minimumFractionDigits: 2 })}
              </span>
            </div>
            <div className="stat-item">
              <strong>Años Disponibles:</strong>
              <span className="stat-value">{stats.years.join(', ')}</span>
            </div>
            <div className="stat-item">
              <strong>Periodos Disponibles:</strong>
              <span className="stat-value">{stats.periods.length}</span>
            </div>
          </div>
          {stats.periods.length > 0 && (
            <div className="periods-list">
              <strong>Periodos:</strong>
              <div className="periods-grid">
                {stats.periods.slice(0, 20).map((periodo, idx) => (
                  <span key={idx} className="periodo-badge">{periodo}</span>
                ))}
                {stats.periods.length > 20 && (
                  <span className="periodo-more">+{stats.periods.length - 20} más</span>
                )}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Filtros y Consulta */}
      <div className="filters-container">
        <h3>🔍 Consultar Datos</h3>
        <div className="filters-form">
          <div className="filter-group">
            <label htmlFor="año">Año (opcional):</label>
            <input
              type="number"
              id="año"
              name="año"
              value={filters.año}
              onChange={handleFilterChange}
              placeholder="2024"
              min="2000"
              max="2100"
              className="filter-input"
            />
          </div>

          <div className="filter-group">
            <label htmlFor="periodo">Periodo AAAAMM (opcional):</label>
            <input
              type="number"
              id="periodo"
              name="periodo"
              value={filters.periodo}
              onChange={handleFilterChange}
              placeholder="202401"
              className="filter-input"
            />
          </div>

          <div className="filter-group">
            <label htmlFor="limit">Límite de registros:</label>
            <input
              type="number"
              id="limit"
              name="limit"
              value={filters.limit}
              onChange={handleFilterChange}
              min="1"
              max="10000"
              className="filter-input"
            />
          </div>

          <button onClick={loadData} disabled={loading} className="query-button">
            {loading ? '⏳ Cargando...' : '🔍 Consultar Datos'}
          </button>
        </div>
      </div>

      {/* Resultados */}
      {error && (
        <div className="error-message">
          <strong>❌ Error:</strong> {error}
        </div>
      )}

      {data && (
        <div className="results-container">
          <h3>📋 Resultados</h3>
          <div className="results-info">
            <span><strong>Total encontrados:</strong> {data.total}</span>
            <span><strong>Mostrando:</strong> {data.data.length}</span>
            {data.has_more && <span className="has-more">⚠️ Hay más registros disponibles</span>}
          </div>

          {data.data.length > 0 ? (
            <div className="table-container">
              <table className="data-table">
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Periodo</th>
                    <th>Código Cuenta</th>
                    <th>Nombre Cuenta</th>
                    <th>Identificación</th>
                    <th>Nombre Tercero</th>
                    <th>Saldo Inicial</th>
                    <th>Movimiento</th>
                    <th>Saldo Final</th>
                    <th>Fecha</th>
                  </tr>
                </thead>
                <tbody>
                  {data.data.map((row) => (
                    <tr key={row.id}>
                      <td>{row.id}</td>
                      <td>{row.periodo}</td>
                      <td>{row.codigo_cuenta_contable}</td>
                      <td className="text-cell">{row.nombre_cuenta_contable?.substring(0, 30)}...</td>
                      <td>{row.identificacion}</td>
                      <td className="text-cell">{row.nombre_tercero?.substring(0, 25)}...</td>
                      <td className="number-cell">
                        {row.saldo_inicial?.toLocaleString('es-ES', { minimumFractionDigits: 2 })}
                      </td>
                      <td className="number-cell">
                        {row.movimiento?.toLocaleString('es-ES', { minimumFractionDigits: 2 })}
                      </td>
                      <td className="number-cell">
                        {row.saldo_final?.toLocaleString('es-ES', { minimumFractionDigits: 2 })}
                      </td>
                      <td>{row.fecha}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <div className="no-data">
              No se encontraron registros con los filtros especificados.
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default DataViewer;

