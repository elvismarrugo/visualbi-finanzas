import React, { useState } from 'react';
import axios from 'axios';
import './DateRangeProcessor.css';

const DateRangeProcessor = () => {
  const [fechaInicio, setFechaInicio] = useState('');
  const [fechaFin, setFechaFin] = useState('');
  const [includesTaxDiff, setIncludesTaxDiff] = useState(false);
  const [clearExisting, setClearExisting] = useState(true);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await axios.post(
        'http://localhost:8000/api/etl/process-date-range',
        {
          fecha_inicio: fechaInicio,
          fecha_fin: fechaFin,
          includes_tax_diff: includesTaxDiff,
          clear_existing: clearExisting
        },
        {
          headers: {
            'Content-Type': 'application/json'
          },
          timeout: 600000 // 10 minutos para procesar muchos periodos
        }
      );

      setResult(response.data);
    } catch (err) {
      console.error('Error completo:', err);
      if (err.response) {
        // El servidor respondió con un error
        setError(`Error ${err.response.status}: ${err.response.data.detail || err.response.data.message || 'Error desconocido'}`);
      } else if (err.request) {
        // La petición se hizo pero no hubo respuesta
        setError(`Error: No se pudo conectar con el servidor en http://localhost:8000. Verifica que el backend esté corriendo. Detalles: ${err.message}`);
      } else {
        // Error al configurar la petición
        setError(`Error: ${err.message}`);
      }
    } finally {
      setLoading(false);
    }
  };

  // Formatear fecha para mostrar
  const formatDate = (dateString) => {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toLocaleDateString('es-ES', { 
      year: 'numeric', 
      month: '2-digit', 
      day: '2-digit' 
    });
  };

  return (
    <div className="date-range-processor">
      <div className="processor-header">
        <h2>📅 Procesar por Rango de Fechas</h2>
        <p className="subtitle">
          Procesa automáticamente todos los periodos entre las fechas que indiques
        </p>
      </div>

      <form onSubmit={handleSubmit} className="processor-form">
        <div className="form-group">
          <label htmlFor="fechaInicio">
            Fecha de Inicio <span className="required">*</span>
          </label>
          <input
            type="date"
            id="fechaInicio"
            value={fechaInicio}
            onChange={(e) => setFechaInicio(e.target.value)}
            required
            min="2000-01-01"
            max="2100-12-31"
            className="date-input"
          />
          <small className="help-text">
            Fecha inicial del rango a procesar (ej: 2024-01-31)
          </small>
        </div>

        <div className="form-group">
          <label htmlFor="fechaFin">
            Fecha de Fin <span className="required">*</span>
          </label>
          <input
            type="date"
            id="fechaFin"
            value={fechaFin}
            onChange={(e) => setFechaFin(e.target.value)}
            required
            min={fechaInicio || "2000-01-01"}
            max="2100-12-31"
            className="date-input"
          />
          <small className="help-text">
            Fecha final del rango a procesar (ej: 2025-09-30)
          </small>
        </div>

        <div className="form-group checkbox-group">
          <label>
            <input
              type="checkbox"
              checked={includesTaxDiff}
              onChange={(e) => setIncludesTaxDiff(e.target.checked)}
            />
            Incluir diferencia de impuestos
          </label>
        </div>

        <div className="form-group checkbox-group">
          <label>
            <input
              type="checkbox"
              checked={clearExisting}
              onChange={(e) => setClearExisting(e.target.checked)}
            />
            Limpiar datos existentes antes de procesar
          </label>
        </div>

        <button 
          type="submit" 
          disabled={loading || !fechaInicio || !fechaFin}
          className="submit-button"
        >
          {loading ? '⏳ Procesando...' : '🚀 Procesar Rango de Fechas'}
        </button>
      </form>

      {error && (
        <div className="error-message">
          <strong>❌ Error:</strong> {error}
        </div>
      )}

      {result && (
        <div className="result-container">
          <h3>✅ Resultado del Procesamiento</h3>
          
          <div className="result-summary">
            <div className="result-item">
              <strong>Fecha Inicio:</strong> {formatDate(result.fecha_inicio)}
            </div>
            <div className="result-item">
              <strong>Fecha Fin:</strong> {formatDate(result.fecha_fin)}
            </div>
            <div className="result-item">
              <strong>Periodos Procesados:</strong> {result.total_periodos}
            </div>
            <div className="result-item">
              <strong>Total de Registros:</strong> {result.total_rows.toLocaleString()}
            </div>
            <div className="result-item">
              <strong>Estado:</strong> 
              <span className={result.success ? 'success' : 'warning'}>
                {result.success ? '✅ Éxito' : '⚠️ Con errores'}
              </span>
            </div>
          </div>

          {result.periodos_procesados && result.periodos_procesados.length > 0 && (
            <div className="periodos-list">
              <h4>Periodos Procesados:</h4>
              <div className="periodos-grid">
                {result.periodos_procesados.map((periodo, index) => (
                  <span key={index} className="periodo-badge">{periodo}</span>
                ))}
              </div>
            </div>
          )}

          {result.errors && result.errors.length > 0 && (
            <div className="errors-list">
              <h4>⚠️ Errores:</h4>
              <ul>
                {result.errors.map((error, index) => (
                  <li key={index}>{error}</li>
                ))}
              </ul>
            </div>
          )}

          <div className="result-actions">
            <button 
              onClick={() => window.location.href = 'http://localhost:8000/docs'}
              className="view-api-button"
            >
              📚 Ver en Swagger UI
            </button>
            <button 
              onClick={() => setResult(null)}
              className="clear-button"
            >
              Limpiar Resultado
            </button>
          </div>
        </div>
      )}

      {loading && (
        <div className="loading-overlay">
          <div className="loading-spinner"></div>
          <p>Procesando periodos... Esto puede tardar varios minutos.</p>
          <p className="loading-note">
            El sistema está descargando y procesando cada mes secuencialmente.
          </p>
        </div>
      )}
    </div>
  );
};

export default DateRangeProcessor;

