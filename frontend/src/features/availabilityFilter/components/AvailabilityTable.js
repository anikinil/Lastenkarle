import React from "react";

import './AvailabilityTable.css';

import { useTranslation } from 'react-i18next';

const AvailabilityTable = ({ bikes, availabilities }) => {

    const currentDate = new Date();
    const daysToShow = 30; // Number of days to display

    const { t } = useTranslation();

    const isAvailableOnDate = (bikeId, date) => {
        const bikeAvs = availabilities.filter(availability => availability.bike === bikeId);
        return !bikeAvs.some(availability => {
            const start = new Date(availability.from_date);
            const end = new Date(availability.until_date);
            return date >= start && date <= end;
        });
    };

    const availabilityData = bikes.map(bike => {
        return Array(daysToShow).fill(null).map((_, index) => {
            const date = new Date(currentDate);
            date.setDate(currentDate.getDate() + index);
            return isAvailableOnDate(bike.id, date) ? "available" : "unavailable";
        });
    });

    const getDayLabels = () => {
        return Array(daysToShow).fill(null).map((_, index) => {
            const date = new Date(currentDate);
            date.setDate(currentDate.getDate() + index);
            return { day: date.getDate(), month: date.toLocaleString("default", { month: "short" }) };
        });
    };

    const dayLabels = getDayLabels();

    return (
        <div className="availability-table-container">
            <div className="overflow-x-auto">
                <table className="availability-table">
                    <thead>
                        <tr>
                            <th rowSpan={2}>{t('bike')}</th>
                            <th rowSpan={2}>{t('store')}</th>
                            {Array.from(new Set(dayLabels.map(label => label.month))).map((month, index) => {
                                const span = dayLabels.filter(label => label.month === month).length;
                                return (
                                    <th key={index} colSpan={span}>
                                        {month}
                                    </th>
                                );
                            })}
                        </tr>
                        <tr>
                            {dayLabels.map((label, index) => (
                                <th key={index}>
                                    {label.day}
                                </th>
                            ))}
                        </tr>
                    </thead>
                    <tbody>
                        {bikes.map((bike, rowIdx) => (
                            <tr key={rowIdx}>
                                <td>{bike.name}</td>
                                <td>{bike.store}</td>
                                {availabilityData[rowIdx].map((status, colIdx) => (
                                    <td key={colIdx}>
                                        <div className={`square`} status={status} />
                                    </td>
                                ))}
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default AvailabilityTable;
