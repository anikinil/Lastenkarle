// Calendar for page of a singular bike
// TODO: Reservation Calendar with two months in advance view
// TODO: Legend for Colours (available, booked, closed, unavailable)
import React, { useState } from "react";
import { Calendar } from "@demark-pro/react-booking-calendar";

import "@demark-pro/react-booking-calendar/dist/react-booking-calendar.css";

// CSS Modules, react-booking-calendar-cssmodules.css
// import '@demark-pro/react-booking-calendar/dist/react-booking-calendar-cssmodules.css';

const oneDay = 86400000;
const today = new Date().getTime() + oneDay;

const reserved = Array.from({ length: 3 }, (_, i) => {
  const daysCount = Math.floor(Math.random() * (7 - 4) + 3);
  const startDate = new Date(today + oneDay * 8 * i);

  return {
    startDate,
    endDate: new Date(startDate.getTime() + oneDay * daysCount),
  };
});

const BookingCalendar = () => {
  const [selectedDates, setSelectedDates] = useState([]);

  return (
    <Calendar
      selected={selectedDates}
      reserved={reserved}
      onChange={setSelectedDates}
    />
  );
};