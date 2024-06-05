import React from "react";
import { useTranslation } from 'react-i18next';

import '../pages/BikeList.css'

const BikeListItem = ({bike}) => {

    const { t } = useTranslation();
    
    // THINK: how to display different buttons to different roles
    return (
        <div className="list-item" key={bike.id}>
            <p className="label">{bike.name}</p>
            <button type="button" className="button">{t('book')}</button>
        </div>
    );
};
  
export default BikeListItem;