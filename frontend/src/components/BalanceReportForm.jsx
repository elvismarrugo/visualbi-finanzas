import { useState } from 'react'
import axios from 'axios'
import './BalanceReportForm.css'

/**
 * Componente para consultar el reporte de balance por terceros de Siigo
 * 
 * Este componente permite al usuario ingresar los parámetros necesarios
 * para obtener un reporte de balance desde la API de Siigo.
 */
function BalanceReportForm() {
  // Estado para almacenar los valores del formulario
  const [formData, setFormData] = useState({
    year: new Date().getFullYear(), // Año actual por defecto
    monthStart: 1,
    monthEnd: 12,
    accountStart: '',
    accountEnd: '',
    includesTaxDiff: false
  })

  // Estado para manejar la respuesta de la API
  const [reportData, setReportData] = useState(null)
  
  // Estado para manejar errores
  const [error, setError] = useState(null)
  
  // Estado para indicar si se está cargando la petición
  const [loading, setLoading] = useState(false)

  /**
   * Maneja los cambios en los campos del formulario
   * @param {Event} e - Evento del input
   */
  const handleChange = (e) => {
    const { name, value, type, checked } = e.target
    
    // Si es un checkbox, usa 'checked', sino usa 'value'
    const inputValue = type === 'checkbox' ? checked : value
    
    // Convierte a número si el campo es numérico
    const finalValue = (name === 'year' || name === 'monthStart' || name === 'monthEnd')
      ? parseInt(inputValue) || 0
      : inputValue

    setFormData(prev => ({
      ...prev,
      [name]: finalValue
    }))
    
    // Limpia errores cuando el usuario modifica el formulario
    if (error) setError(null)
  }

  /**
   * Valida que los datos del formulario sean correctos antes de enviar
   * @returns {boolean} - true si la validación es exitosa
   */
  const validateForm = () => {
    if (!formData.year || formData.year < 2000 || formData.year > 2100) {
      setError('El año debe estar entre 2000 y 2100')
      return false
    }

    if (formData.monthStart < 1 || formData.monthStart > 13) {
      setError('El mes de inicio debe estar entre 1 y 13')
      return false
    }

    if (formData.monthEnd < 1 || formData.monthEnd > 13) {
      setError('El mes de fin debe estar entre 1 y 13')
      return false
    }

    if (formData.monthStart > formData.monthEnd) {
      setError('El mes de inicio no puede ser mayor al mes de fin')
      return false
    }

    // accountStart y accountEnd son opcionales según la API de Siigo

    return true
  }

  /**
   * Maneja el envío del formulario y la petición a la API
   * @param {Event} e - Evento del formulario
   */
  const handleSubmit = async (e) => {
    e.preventDefault() // Previene el comportamiento por defecto del formulario
    
    // Limpia estados anteriores
    setError(null)
    setReportData(null)

    // Valida el formulario antes de enviar
    if (!validateForm()) {
      return
    }

    setLoading(true) // Indica que la petición está en proceso

    try {
      // Realiza la petición POST al backend
      // El backend está configurado para correr en http://localhost:8000
      // Construir el payload, solo incluir account_start y account_end si tienen valor
      const payload = {
        year: formData.year,
        month_start: formData.monthStart,
        month_end: formData.monthEnd,
        includes_tax_diff: formData.includesTaxDiff
      }

      // Agregar account_start y account_end solo si tienen valor (son opcionales)
      if (formData.accountStart && formData.accountStart.trim()) {
        payload.account_start = formData.accountStart.trim()
      }
      if (formData.accountEnd && formData.accountEnd.trim()) {
        payload.account_end = formData.accountEnd.trim()
      }

      const response = await axios.post(
        'http://localhost:8000/api/balance-report-by-thirdparty',
        payload,
        {
          headers: {
            'Content-Type': 'application/json'
          }
        }
      )

      // Si la petición es exitosa, guarda los datos
      setReportData(response.data)
      
    } catch (err) {
      // Maneja diferentes tipos de errores
      if (err.response) {
        // Error de respuesta del servidor (4xx, 5xx)
        setError(err.response.data?.detail || 'Error al obtener el reporte')
      } else if (err.request) {
        // Error de red (no se recibió respuesta)
        setError('❌ No se pudo conectar con el servidor backend. El backend no está corriendo en http://localhost:8000. Por favor, inicia el backend ejecutando: cd backend && python3 main.py')
      } else {
        // Otro tipo de error
        setError('Ocurrió un error inesperado: ' + err.message)
      }
    } finally {
      // Siempre desactiva el estado de carga, sin importar el resultado
      setLoading(false)
    }
  }

  return (
    <div className="balance-report-form-container">
      <form onSubmit={handleSubmit} className="balance-report-form">
        <h2>Reporte de Balance por Terceros</h2>
        <p className="form-description">
          Completa los siguientes campos para obtener el reporte de balance desde Siigo
        </p>

        {/* Campo: Año */}
        <div className="form-group">
          <label htmlFor="year">
            Año <span className="required">*</span>
          </label>
          <input
            type="number"
            id="year"
            name="year"
            value={formData.year}
            onChange={handleChange}
            min="2000"
            max="2100"
            required
            placeholder="Ej: 2024"
          />
        </div>

        {/* Campos: Mes de inicio y fin */}
        <div className="form-row">
          <div className="form-group">
            <label htmlFor="monthStart">
              Mes de Inicio <span className="required">*</span>
            </label>
            <input
              type="number"
              id="monthStart"
              name="monthStart"
              value={formData.monthStart}
              onChange={handleChange}
              min="1"
              max="13"
              required
              placeholder="1-13"
            />
          </div>

          <div className="form-group">
            <label htmlFor="monthEnd">
              Mes de Fin <span className="required">*</span>
            </label>
            <input
              type="number"
              id="monthEnd"
              name="monthEnd"
              value={formData.monthEnd}
              onChange={handleChange}
              min="1"
              max="13"
              required
              placeholder="1-13"
            />
          </div>
        </div>

        {/* Campos: Cuenta inicial y final */}
        <div className="form-row">
          <div className="form-group">
            <label htmlFor="accountStart">
              Código de Cuenta Inicial <span className="optional">(Opcional)</span>
            </label>
            <input
              type="text"
              id="accountStart"
              name="accountStart"
              value={formData.accountStart}
              onChange={handleChange}
              placeholder="Ej: 1105"
            />
          </div>

          <div className="form-group">
            <label htmlFor="accountEnd">
              Código de Cuenta Final <span className="optional">(Opcional)</span>
            </label>
            <input
              type="text"
              id="accountEnd"
              name="accountEnd"
              value={formData.accountEnd}
              onChange={handleChange}
              placeholder="Ej: 1199"
            />
          </div>
        </div>

        {/* Checkbox: Incluir diferencia de impuestos */}
        <div className="form-group checkbox-group">
          <label htmlFor="includesTaxDiff" className="checkbox-label">
            <input
              type="checkbox"
              id="includesTaxDiff"
              name="includesTaxDiff"
              checked={formData.includesTaxDiff}
              onChange={handleChange}
            />
            <span>Incluir diferencia de impuestos <span className="required">*</span></span>
          </label>
        </div>

        {/* Botón de envío */}
        <button 
          type="submit" 
          className="submit-button"
          disabled={loading}
        >
          {loading ? 'Consultando...' : 'Obtener Reporte'}
        </button>

        {/* Mensaje de error */}
        {error && (
          <div className="error-message">
            <strong>Error:</strong> {error}
          </div>
        )}
      </form>

      {/* Sección de resultados */}
      {reportData && (
        <div className="report-results">
          <h3>Resultados del Reporte</h3>
          
          {/* Si hay file_url, mostrar botón de descarga */}
          {reportData.file_url && (
            <div className="download-section">
              <a 
                href={reportData.file_url} 
                target="_blank" 
                rel="noopener noreferrer"
                className="download-button"
              >
                📥 Descargar Reporte Excel
              </a>
              {reportData.file_id && (
                <p className="file-info">ID del archivo: {reportData.file_id}</p>
              )}
            </div>
          )}
          
          <details className="report-details">
            <summary>Ver respuesta completa de la API</summary>
            <pre className="report-data">
              {JSON.stringify(reportData, null, 2)}
            </pre>
          </details>
        </div>
      )}
    </div>
  )
}

export default BalanceReportForm

