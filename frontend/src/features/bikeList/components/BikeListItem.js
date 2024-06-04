import React from "react";
import { useTranslation } from 'react-i18next';

import '../pages/BikeList.css'

const BikeListItem = ({bike, index}) => {

    const { t } = useTranslation();

    return (

        // FIXME: perhaps add separate panels for each list item

        // LEARN: think about how to display different buttons to different roles

        <div className="list-item" key={index}>
            <p className="label">{bike.name}</p>
            <button type="button" className="button">{t('book')}</button>
        </div>
    );
};
  
export default BikeListItem;