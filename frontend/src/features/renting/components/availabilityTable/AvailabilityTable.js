import React from "react";

import './AvailabilityTable.css';

import { useTranslation } from 'react-i18next';
import { BIKE_RENTING, STORE_PAGE_OF_BIKE } from "../../../../constants/URLs/Navigation";
import { ID } from "../../../../constants/URLs/General";
import i18n from "../../../../i18n";

const AvailabilityTable = ({ bikes, availabilities, from, to }) => {

    const defaultNumDays = 21; // Number of days to display per default

    const { t } = useTranslation();

    const isAvailableOnDate = (bikeId, date) => {
        const normalizeDate = (d) => new Date(d.getFullYear(), d.getMonth(), d.getDate());
        const normalizedDate = normalizeDate(date);

        const bikeAvs = availabilities.filter(availability => availability.bike === bikeId);
        return !bikeAvs.some(availability => {
            const start = normalizeDate(new Date(availability.from_date));
            const end = normalizeDate(new Date(availability.until_date));
            return normalizedDate >= start && normalizedDate <= end;
        });
    };

    const getDatesToShow = () => {
        const currentDate = new Date();
        currentDate.setHours(0, 0, 0, 0);

        if (from && to) {
            const fromDate = new Date(from);
            const toDate = new Date(to);
            const days = (toDate - fromDate) / (1000 * 60 * 60 * 24) + 1;
            return Array.from({ length: days }, (_, index) => {
                const date = new Date(fromDate);
                date.setDate(fromDate.getDate() + index);
                return date;
            });
        } else {
            return Array.from({ length: defaultNumDays }, (_, index) => {
                const date = new Date(currentDate);
                date.setDate(currentDate.getDate() + index);
                return date;
            });
        }
    };

    const getAvailabilityData = () => {
        const allBikeData = bikes.map(bike => {
            return {
                id: bike.id,
                store: bike.store,
                name: bike.name,
                avs: getDatesToShow().map(date => {
                    return isAvailableOnDate(bike.id, date) ? 'available' : 'unavailable';
                })
            };
        });
        return allBikeData.filter((bike) => bike.avs.some(av => av === 'available'));
    };


    const getDayLabels = () => {
        const locale = i18n.language;
        return getDatesToShow().map(date => {
            return {
                day: date.getDate(),
                month: date.toLocaleString(locale, { month: "short" }),
                weekday: date.toLocaleString(locale, { weekday: "short" })
            };
        });
    };

    const dayLabels = getDayLabels();

    return (
        <div className="availability-table-container">
            <div className="overflow-x-auto">
                <table className="availability-table">
                    {getAvailabilityData().length === 0 ?
                        <p>{t('no_bikes_available_at_selected_period')}</p>
                        :
                        <>
                            <thead>
                                <tr>
                                    <th rowSpan={3}>{t('bike')}</th>
                                    <th rowSpan={3}>{t('store')}</th>
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
                                <tr>
                                    {dayLabels.map((label, index) => (
                                        <th key={index}>
                                            {label.weekday}
                                        </th>
                                    ))}
                                </tr>
                            </thead>
                            <tbody>
                                {getAvailabilityData().map((bike, rowIdx) => (
                                    <tr key={rowIdx}>
                                        <td><a href={BIKE_RENTING.replace(ID, bike.id)}>{bike.name}</a></td>
                                        <td><a href={STORE_PAGE_OF_BIKE.replace(ID, bike.id)}>{bike.store}</a></td>
                                        {bike.avs.map((status, colIdx) => (
                                            <td key={colIdx}>
                                                <div className={`square`} status={status} />
                                            </td>
                                        ))}
                                    </tr>
                                ))}
                            </tbody>
                        </>
                    }
                </table>
            </div>
        </div>
    );
};

export default AvailabilityTable;
