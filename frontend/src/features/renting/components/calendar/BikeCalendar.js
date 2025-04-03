import React, { useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';
import './BikeCalendar.css';
import i18n from 'i18next';

import { useNotification } from '../../../../components/notifications/NotificationContext';
import { getCookie } from '../../../../services/Cookies';
import { ALL_AVAILABILITIES, AVAILABILITY_OF_BIKE } from '../../../../constants/URIs/RentingURIs';
import { ID } from '../../../../constants/URIs/General';

const getDaysInMonth = (month, year) => new Date(year, month + 1, 0).getDate();
const getCurrLang = () => i18n.language;

const BikeCalendar = ({ bikeId }) => {
    const { t } = useTranslation();
    const { showNotification } = useNotification();

    const today = new Date();
    const currentMonth = today.getMonth();
    const currentYear = today.getFullYear();

    const token = getCookie('token');

    const [selectedStartDate, setSelectedStartDate] = useState(null);
    const [selectedEndDate, setSelectedEndDate] = useState(null);
    const [availability, setAvailability] = useState([]);

    // const fetchAvailability = async () => {
    //     const response = await fetch(AVAILABILITY_OF_BIKE.replace(ID, bikeId), {
    //         headers: {
    //             'Content-Type': 'application/json',
    //             'Authorization': `Token ${token}`
    //         }
    //     });
    //     const data = await response.json();
    //     setAvailability(data);
    // };

    const fetchAvailability = () => {
        fetch(AVAILABILITY_OF_BIKE.replace(ID, bikeId), {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${token}`
            }
        })
        .then(response => response.json())
        .then(data => {
            setAvailability(data)
        })
        .catch(error => {
            console.error("ERROR", error)
        })
    }


    const handleDayClick = (date) => {
        const dateString = date.toISOString().split('T')[0];

        if (availability[dateString] !== 0) return;

        if (!selectedStartDate || (selectedStartDate && selectedEndDate)) {
            setSelectedStartDate(date);
            setSelectedEndDate(null);
        } else if (selectedStartDate && !selectedEndDate) {
            if (date >= selectedStartDate) {
                setSelectedEndDate(date);
            } else {
                setSelectedStartDate(date);
            }
        }
    };

    const postBooking = async () => {
        if (!selectedStartDate || !selectedEndDate) {
            showNotification(t('select_dates_first'), 'error');
            return;
        }

        const payload = {
            begin: selectedStartDate.toISOString().split('T')[0],
            end: selectedEndDate.toISOString().split('T')[0],
            equipment: []
        };

        try {
            const response = await fetch(`/api/booking/v1/bikes/${bikeId}/booking`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Token ${token}`
                },
                body: JSON.stringify(payload)
            });

            if (response.ok) {
                showNotification(t('booking_successful'), 'success');
                // fetchAvailability(); // Refresh availabiliy
                setSelectedStartDate(null);
                setSelectedEndDate(null);
            } else {
                const error = await response.json();
                throw new Error(error.detail);
            }
        } catch (error) {
            showNotification(`${t('booking_failed')}: ${error.message}`, 'error');
        }
    };

    console.log(availability)

    const renderCalendarDays = (month, year) => {
        const daysInMonth = getDaysInMonth(month, year);
        const firstDay = new Date(year, month, 1).getDay();
        const firstDayIndex = firstDay === 0 ? 6 : firstDay - 1;
        const daysArray = Array.from({ length: daysInMonth }, (_, i) => new Date(year, month, i + 1));

        return (
            <>
                {["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"].map((d, i) => (
                    <div key={i} className="weekday-label">{d}</div>
                ))}
                {Array.from({ length: firstDayIndex }).map((_, i) => (
                    <div key={`empty-${i}`} className="calendar-day empty"></div>
                ))}
                {daysArray.map((day) => {
                    const dateString = day.toISOString().split('T')[0];
                    const isSelectedStart = selectedStartDate?.toISOString().split('T')[0] === dateString;
                    const isSelectedEnd = selectedEndDate?.toISOString().split('T')[0] === dateString;

                    let dayClass = '';
                    if (availability[dateString] === 0) dayClass = 'available';
                    else if (availability[dateString] === 1) dayClass = 'reserved';
                    else if (availability[dateString] === 2) dayClass = 'closed';
                    else dayClass = 'not-bookable';

                    if (isSelectedStart || isSelectedEnd) {
                        dayClass += ' selected';
                    }

                    return (
                        <div
                            key={dateString}
                            className={`calendar-day ${dayClass}`}
                            onClick={() => handleDayClick(day)}
                        >
                            {day.getDate()}
                        </div>
                    );
                })}
            </>
        );
    };

    useEffect(() => {
        fetchAvailability();
    }, []);

    return (
        <div className="booking-calendar">
            <div className="month-container-wrapper">
                <div className="month-container">
                    <h2>{new Date(currentYear, currentMonth).toLocaleString(getCurrLang(), { month: 'long' })} {currentYear}</h2>
                    <div className="calendar-grid">
                        {renderCalendarDays(currentMonth, currentYear)}
                    </div>
                </div>

                <div className="month-container">
                    <h2>{new Date(currentYear, currentMonth + 1).toLocaleString(getCurrLang(), { month: 'long' })} {currentYear}</h2>
                    <div className="calendar-grid">
                        {renderCalendarDays(currentMonth + 1, currentYear)}
                    </div>
                </div>
            </div>

            <div className="selection-info">
                <p>{t('pickup_date')}: {selectedStartDate ? selectedStartDate.toDateString() : t('select_date')}</p>
                <p>{t('return_date')}: {selectedEndDate ? selectedEndDate.toDateString() : t('select_date')}</p>
            </div>

            <div className="legend">
                <p><span className="legend-color available"></span> Buchbar</p>
                <p><span className="legend-color reserved"></span> Reserviert</p>
                <p><span className="legend-color closed"></span> Standort geschlossen</p>
                <p><span className="legend-color not-bookable"></span> Nicht buchbar</p>
            </div>

            <button onClick={postBooking} className="booking-button">
                {t('book_now')}
            </button>
        </div>
    );
};

export default BikeCalendar;