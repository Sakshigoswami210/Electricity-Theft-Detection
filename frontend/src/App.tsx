import { useEffect, useState } from 'react'
import axios from 'axios'
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  ReferenceDot,
} from 'recharts'

interface AnomalyEvent {
  Meter_ID: number
  Anomaly_Group: number
  Start_Time: string
  End_Time: string
  Number_of_Anomalies: number
  Maximum_Consumption_Wh: number
  Maximum_Anomaly_Score: number
  Maximum_Deviation_Wh: number
  Duration_Hours: number
  Investigation_Priority: string
}

interface AnomalyResponse {
  total_events: number
  events: AnomalyEvent[]
}

interface MeterReading {
  Meter_ID: number
  Datetime: string
  Total_Consumption_Wh: number
  Average_Voltage_V: number
  Consumption_Change_Wh: number
  Rolling_24h_Mean: number
  Rolling_24h_Std: number
  Consumption_Deviation: number
  Hour: number
  Day_of_Week: number
  Is_Weekend: number
  Anomaly_Score: number
  Final_Anomaly_Flag: number
}

interface MeterReadingResponse {
  meter_id: number
  total_readings: number
  readings: MeterReading[]
}

function App() {
  const [events, setEvents] = useState<AnomalyEvent[]>([])
  const [readings, setReadings] = useState<MeterReading[]>([])
  const [selectedMeter, setSelectedMeter] = useState('all')
  const [startDate, setStartDate] = useState('')
  const [endDate, setEndDate] = useState('')
  const [loading, setLoading] = useState(true)
  const [readingsLoading, setReadingsLoading] = useState(false)
  const [error, setError] = useState('')
  const [readingsError, setReadingsError] = useState('')

  useEffect(() => {
    setLoading(true)
    setError('')

    const url =
      selectedMeter === 'all'
        ? 'http://127.0.0.1:8000/anomalies'
        : `http://127.0.0.1:8000/anomalies/${selectedMeter}`

    axios
      .get<AnomalyResponse>(url)
      .then((response) => {
        setEvents(response.data.events)
        setLoading(false)
      })
      .catch(() => {
        setError('Unable to load anomaly data from the backend.')
        setLoading(false)
      })
  }, [selectedMeter])

  useEffect(() => {
    if (selectedMeter === 'all') {
      setReadings([])
      return
    }

    setReadingsLoading(true)
    setReadingsError('')

    axios
      .get<MeterReadingResponse>(
        `http://127.0.0.1:8000/meter-readings/${selectedMeter}`
      )
      .then((response) => {
        setReadings(response.data.readings)
        setReadingsLoading(false)
      })
      .catch(() => {
        setReadingsError('Unable to load meter readings.')
        setReadingsLoading(false)
      })
  }, [selectedMeter])

  const meters = new Set(events.map((event) => event.Meter_ID)).size

  const filteredReadings = readings.filter((reading) => {
  const readingDate = reading.Datetime.slice(0, 10)

  if (startDate && readingDate < startDate) {
    return false
  }

  if (endDate && readingDate > endDate) {
    return false
  }

  return true
})

const chartData = filteredReadings.map((reading) => ({
  time: reading.Datetime,
  consumption: reading.Total_Consumption_Wh,
  anomaly:
    reading.Final_Anomaly_Flag === 1
      ? reading.Total_Consumption_Wh
      : null,
}))

  return (
    <div className="dashboard">
      <header className="header">
        <div>
          <h1>Electricity Anomaly Monitoring</h1>
          <p>Smart Meter Consumption Analysis & Anomaly Detection</p>
        </div>

        <div className="status">
          <span className="status-dot"></span>
          System Active
        </div>
      </header>

      <section className="summary-cards">
        <div className="card">
          <h3>Total Anomaly Events</h3>
          <p>{events.length.toLocaleString()}</p>
        </div>

        <div className="card">
          <h3>Meters With Events</h3>
          <p>{meters}</p>
        </div>

        <div className="card">
          <h3>Detection Method</h3>
          <p>Isolation Forest</p>
        </div>

        <div className="card">
          <h3>Status</h3>
          <p>Review Required</p>
        </div>
      </section>

      <section className="meter-section">
        <label htmlFor="meter">Select Meter</label>

        <select
          id="meter"
          value={selectedMeter}
          onChange={(event) => setSelectedMeter(event.target.value)}
        >
          <option value="all">All Meters</option>

          {[...new Set(events.map((event) => event.Meter_ID))]
            .sort((a, b) => a - b)
            .map((meter) => (
              <option key={meter} value={meter}>
                Meter {meter}
              </option>
            ))}
        </select>
      </section>

      {selectedMeter !== 'all' && (
  <section className="date-filter">
    <div>
      <label htmlFor="start-date">Start Date</label>
      <input
        id="start-date"
        type="date"
        value={startDate}
        onChange={(event) => setStartDate(event.target.value)}
      />
    </div>

    <div>
      <label htmlFor="end-date">End Date</label>
      <input
        id="end-date"
        type="date"
        value={endDate}
        onChange={(event) => setEndDate(event.target.value)}
      />
    </div>

    <button
      onClick={() => {
        setStartDate('')
        setEndDate('')
      }}
    >
      Clear Dates
    </button>
  </section>
)}

      {selectedMeter !== 'all' && (
        <section className="chart-section">
          <div className="section-header">
            <h2>Consumption Trend - Meter {selectedMeter}</h2>
            <span>Hourly electricity consumption</span>
          </div>

          {readingsLoading && <p>Loading meter readings...</p>}

          {readingsError && <p>{readingsError}</p>}

          {!readingsLoading && !readingsError && readings.length > 0 && (
            <div
              style={{
                width: '100%',
                height: '450px',
              }}
            >
              <ResponsiveContainer width="100%" height="100%">
                <LineChart
                  data={chartData}
                  margin={{
                    top: 20,
                    right: 30,
                    left: 20,
                    bottom: 60,
                  }}
                >
                  <CartesianGrid strokeDasharray="3 3" />

                  <XAxis
                    dataKey="time"
                    angle={-45}
                    textAnchor="end"
                    height={80}
                    interval="preserveStartEnd"
                  />

                  <YAxis
                    label={{
                      value: 'Consumption (Wh)',
                      angle: -90,
                      position: 'insideLeft',
                    }}
                  />

                  <Tooltip />

                  <Line
                    type="monotone"
                    dataKey="consumption"
                    stroke="#2563eb"
                    dot={false}
                    strokeWidth={2}
                    name="Consumption"
                  />

                  {chartData.map((point, index) =>
                    point.anomaly !== null ? (
                      <ReferenceDot
                        key={`anomaly-${index}`}
                        x={point.time}
                        y={point.anomaly}
                        r={5}
                        fill="#dc2626"
                        stroke="#dc2626"
                      />
                    ) : null
                  )}
                </LineChart>
              </ResponsiveContainer>
            </div>
          )}

          {!readingsLoading &&
            !readingsError &&
            readings.length === 0 && (
              <p>No meter readings available.</p>
            )}

          <div className="chart-info">
            <span>
              ● Blue line = Electricity consumption
            </span>
            <span>
              ● Red points = Detected anomalies
            </span>
          </div>
        </section>
      )}

      <section className="events-section">
        <div className="section-header">
          <h2>Anomaly Events</h2>
          <span>Unusual consumption requiring review</span>
        </div>

        {loading && <p>Loading anomaly data...</p>}

        {error && <p>{error}</p>}

        {!loading && !error && (
          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>Meter</th>
                  <th>Start Time</th>
                  <th>End Time</th>
                  <th>Max Consumption</th>
                  <th>Deviation</th>
                  <th>Anomaly Score</th>
                  <th>Status</th>
                </tr>
              </thead>

              <tbody>
                {events.map((event) => (
                  <tr
                    key={`${event.Meter_ID}-${event.Anomaly_Group}-${event.Start_Time}`}
                  >
                    <td>{event.Meter_ID}</td>

                    <td>{event.Start_Time}</td>

                    <td>{event.End_Time}</td>

                    <td>
                      {event.Maximum_Consumption_Wh.toFixed(2)} Wh
                    </td>

                    <td>
                      {event.Maximum_Deviation_Wh.toFixed(2)} Wh
                    </td>

                    <td>
                      {event.Maximum_Anomaly_Score.toFixed(4)}
                    </td>

                    <td>
                      <span className="review">
                        {event.Investigation_Priority}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>

      <footer>
        <p>
          Anomaly detection identifies unusual consumption patterns. It does
          not confirm electricity theft.
        </p>
      </footer>
    </div>
  )
}

export default App