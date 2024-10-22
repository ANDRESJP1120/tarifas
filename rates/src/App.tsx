import React, { useState } from 'react';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';
import './App.css';

function App(): JSX.Element {
  const [startDate, setStartDate] = useState<Date>(new Date());
  const [showReport, setShowReport] = useState(false);

  const CustomInput: React.FC<{ value?: string; onClick?: () => void }> = ({ value, onClick }) => (
    <button className="custom-btn" onClick={onClick}>
      <svg width="16" height="16" viewBox="0 0 99 100" fill="none" xmlns="http://www.w3.org/2000/svg" className="svg-icon">
        <path d="M86.625 20.5958C86.625 16.1333 83.028 12.5 78.6101 12.5H20.3899C15.972 12.5 12.375 16.1333 12.375 20.5958V26.2292H17.8448V20.5958C17.8448 19.1792 18.9832 18.025 20.3899 18.025H78.606C80.0085 18.025 81.1511 19.1792 81.1511 20.5958V31.2H12.375V79.4C12.375 83.8667 15.972 87.5 20.3899 87.5H78.606C83.028 87.5 86.625 83.8667 86.625 79.4042V43.4333H81.1553V79.4042C81.1553 80.8208 80.0126 81.975 78.6101 81.975H20.3899C18.9832 81.975 17.8448 80.8208 17.8448 79.4042V36.7292H86.625V20.5958Z" fill="white"/>
        <path d="M74.6271 55.5581V50.0289H66.7814V43.4414H61.3075V50.0289H51.5725V43.4414H46.0986V50.0289H36.3595V43.4414H30.8898V50.0289H24.364V55.5581H30.8898V63.3914H24.364V68.9164H30.8898V75.5039H36.3595V68.9164H46.0945V75.5039H51.5684V68.9164H61.3034V75.5039H66.7773V68.9164H74.6189V63.3914H66.7814V55.5581H74.6271ZM36.3595 55.5581H46.0986V63.3914H36.3595V55.5581ZM61.3075 63.3914H51.5725V55.5581H61.3075V63.3914Z" fill="white"/>
      </svg>
      FILTRAR POR FECHA
    </button>
  );

  const handleDownload = () => {
    const month = startDate.getMonth();
    const year = startDate.getFullYear();
    if (year >= 2024 && month >= 1) { // Febrero es el mes 1
      const monthNames = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"];
      const formattedMonth = monthNames[month];
      const formattedYear = year.toString(); // Obtener los últimos dos dígitos del año
      const excelUrl = `${formattedMonth} ${formattedYear}.xlsx`;
      const link = document.createElement('a');
      link.href = `/${excelUrl}`;
      link.download = `${formattedMonth} ${formattedYear}.xlsx`;
      link.click();
    } else {
      alert("Por favor selecciona una fecha válida desde Febrero de 2024 en adelante.");
    }
  };

  const handleDownloadHistorico = () => {
    const link = document.createElement('a');
    link.href = '/Historico de tarifas.xlsx';
    link.download = 'Historico de tarifas.xlsx';
    link.click();
  };

  const handleShowReport = () => {
    setShowReport(!showReport);
  };

  return (
    <div className="container">
      <div className="tarifas-text">
        Recuerda que las tarifas serán publicadas los primeros 10 días de cada mes.
      </div>
      <div className="row">
        <DatePicker
          selected={startDate}
          onChange={(date: Date) => setStartDate(date)}
          dateFormat="yyyy-MM"
          showMonthYearPicker
          customInput={<CustomInput />}
          className="datepicker"
          minDate={new Date(2024, 1, 1)}
          maxDate={new Date(2024, 8, 31)}
        />
        <button className="download-btn" onClick={handleDownload}>DESCARGAR TARIFA DEL MES</button>

        <button className="show-report-btn" onClick={handleShowReport}>
          {showReport ? "Ocultar Reporte" : "HISTORICO DE TARIFAS"}
        </button>
        {showReport && (
          <div id="powerBIContainer" style={{ position: 'fixed', top: 0, left: 0, width: '100%', height: '100%', backgroundColor: 'rgba(0,0,0,0.5)', zIndex: 1000 }}>
            <div style={{ position: 'relative', width: '80%', height: '80%', margin: '5% auto', backgroundColor: '#fff', padding: '10px' }}>
              <iframe
                title="Historico de tarifas"
                width="100%"
                height="100%"
                src="https://app.powerbi.com/reportEmbed?reportId=8e034c61-c319-41bd-b7c4-0f2e13131b4c&autoAuth=true&ctid=d539d4bf-5610-471a-afc2-1c76685cfefa"
                frameBorder="0"
                allowFullScreen={true}
              ></iframe>
              <button onClick={handleShowReport} style={{ position: 'absolute', top: '10px', right: '10px', backgroundColor: '#fff', border: 'none', cursor: 'pointer' }}>
                Cerrar
              </button>
            </div>
          </div>
        )}
        <button className="download-historico-btn" onClick={handleDownloadHistorico}>
          DESCARGAR HISTORICO DE TARIFAS
        </button>
      </div>
    </div>
  );
}

export default App;
