import React, { useState } from "react";
import { useTranslation } from 'react-i18next';

import DayRow from "./DayRow";

import "./StoreOpeningTimesConfig.css"
import 'react-time-picker/dist/TimePicker.css';
import 'react-clock/dist/Clock.css';

const StoreOpeningTimesConfig = () => {

    const { t } = useTranslation();

    const daysOfWeek = [t('monday'), t('tuesday'), t('wednesday'), t('thursday'), t('friday'), t('saturday'), t('sunday')];

    return (
        <>
            <h2>{t('opening_times')}</h2>

            <div className="week-container">
                <div className="header">
                    <span className="header-label"></span> {/* empty on purpose */}
                    <span className="header-label">{t('open')}</span>
                    <span className="header-label">{t('from')}</span>
                    <span className="header-label">{t('to')}</span>
                </div>
                {daysOfWeek.map((day) => (
                    <DayRow key={day} day={day} />
                ))}
            </div>
        </>
    );
};

export default StoreOpeningTimesConfig;