import React from 'react';
import './Loading.css';
import { useTranslation } from 'react-i18next';

const Loading = () => {

    const { t } = useTranslation();

    return (
        <div className="loading-overlay">
            <div className="spinner"></div>
            <p>{t('loading')}</p>
        </div>
    );
};

export default Loading;
