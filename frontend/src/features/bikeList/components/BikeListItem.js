import React from "react";
import { useTranslation } from 'react-i18next';

import '../pages/BikeList.css'

const BikeListItem = ({bike, index}) => {

    const { t } = useTranslation();

    return (
        <div className="list-item" key={index}>
            <p className="label">{bike.name}</p>
            <button type="button" className="button">{t('book')}</button>
        </div>
    );
};
  
export default BikeListItem;