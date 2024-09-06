// Calendar for page of a singular bike
// TODO: Reservation Calendar with two months in advance view
// TODO: Legend for Colours (available, booked, closed, unavailable)
import React, { useState } from 'react';
import Calendar from 'react-calendar';
import 'react-calendar/dist/Calendar.css';
import './BikeCalendar.css'; // Für benutzerdefinierte Styles

const BookingCalendar = () => {
  // Definiere den State für Buchungen
  const [bookings, setBookings] = useState({
    '2024-09-10': 'buchbar',
    '2024-09-11': 'gebucht',
    '2024-09-12': 'standort_geschlossen',
    '2024-09-13': 'nicht_buchbar',
    // weitere Tage und ihre Status
  });

  // Methode, um das Format der Daten anzupassen
  const formatDate = (date) => {
    const year = date.getFullYear();
    const month = (`0${date.getMonth() + 1}`).slice(-2);
    const day = (`0${date.getDate()}`).slice(-2);
    return `${year}-${month}-${day}`;
  };

  // Methode zur Auswahl des Tages und deren Status
  const getDayTileClass = (date) => {
    const formattedDate = formatDate(date);
    return bookings[formattedDate] || ''; // Rückgabe des Status für den jeweiligen Tag
  };

  return (
    <div className="booking-calendar">
      <h3>Buchungskalender für Lastenrad</h3>
      <Calendar
        tileClassName={({ date }) => getDayTileClass(date)}
        view="month"
      />
      <div className="legend">
        <p><span className="buchbar"></span> Buchbar</p>
        <p><span className="gebucht"></span> Gebucht/Gesperrt</p>
        <p><span className="standort_geschlossen"></span> Standort geschlossen</p>
        <p><span className="nicht_buchbar"></span> Nicht buchbar</p>
      </div>
    </div>
  );
};

export default BookingCalendar;