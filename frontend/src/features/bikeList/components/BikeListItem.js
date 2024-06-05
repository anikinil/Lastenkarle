import React from "react";
import { useTranslation } from 'react-i18next';

import '../pages/BikeList.css'

const BikeListItem = ({bike}) => {

    const { t } = useTranslation();
    
    // THINK: how to display different buttons to different roles
    return (
        <li className="list-item">
            <p className="label">{bike.name}</p>
            <button type="button" className="button">{t('book')}</button>
            <div className="img-container">
                <img className="img" alt={bike.name} src={bike.image}></img>
            </div>
        </li>
    );
};
  
export default BikeListItem;