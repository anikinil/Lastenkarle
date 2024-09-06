// Calendar for page of a singular bike
// TODO: Reservation Calendar with two months in advance view
// TODO: Legend for Colours (available, booked, closed, unavailable)
import React, { useState } from 'react';
import Calendar from 'react-calendar';
import 'react-calendar/dist/Calendar.css'; // Standard-Styles von react-calendar importieren

const CalendarComponent = ({ onChange }) => {
    const [date, setDate] = useState(new Date());

    // Mock-Daten direkt im Code
    const availabilities = [
        { date: '2024-07-01', status: 'available' },
        { date: '2024-07-02', status: 'booked' },
        { date: '2024-07-03', status: 'closed' },
        // Weitere Verfügbarkeiten hier...
    ];

    const handleDateChange = (date) => {
        setDate(date);
        onChange(date);
    };

    const tileClassName = ({ date, view }) => {
        if (view === 'month') {
            const dateString = date.toISOString().split('T')[0];
            const availability = availabilities.find(a => a.date === dateString);
            if (availability) {
                if (availability.status === 'available') {
                    return 'react-calendar__tile--available';
                } else if (availability.status === 'booked') {
                    return 'react-calendar__tile--booked';
                } else if (availability.status === 'closed') {
                    return 'react-calendar__tile--closed';
                }
            }
        }
        return '';
    };

    return (
        <div>
            <Calendar
                onChange={handleDateChange}
                value={date}
                tileClassName={tileClassName}
                minDetail='month'
                maxDetail='month'
                activeStartDate={new Date()} // Startdatum ist der aktuelle Monat
            />
        </div>
    );
};

export default CalendarComponent;