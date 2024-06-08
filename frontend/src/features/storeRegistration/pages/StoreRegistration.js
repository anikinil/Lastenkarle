import React, { useState } from "react";
import { useTranslation } from 'react-i18next';

import "./StoreRegistration.css"

const StoreRegistration = () => {

    const { t } = useTranslation();

    const [pictureSelected, setPictureSelected] = useState(false);

    // prevents user from switching to new line by hitting [Enter]
    const handleAddressKeyDown = (event) => {
        if (event.key === 'Enter') {
            event.preventDefault();
        }
    };

    return (
        <>
            <h1>{t('new_store')}</h1>

            <div>
                <div className="new-store-img-container">
                    {pictureSelected ?
                        <img className="new-store-img" alt={t('store_image')} src="source"></img>
                        :
                        <p className="new-store-image-container-label">{t('select_a_picture')}</p>
                    }
                </div>

                <textarea title={t('store_description')} className="new-store-description" placeholder={t('store_description')}></textarea>
            </div>

            <div className="button-container">
                <button type="button" className="button regular">{t('remove_picture')}</button>
            </div>

            <textarea title={t('store_address')} className="new-store-address" rows="1" onKeyDown={handleAddressKeyDown} placeholder={t('store_address')}></textarea>

            <div className="button-container">
                <button type="button" className="button regular">{t('configure_opening_times')}</button>
                <button type="button" className="button regular">{t('assign_bikes')}</button>
            </div>
            
            <div className="button-container">
                <button type="button" className="button accent">{t('register_new_store')}</button>
            </div>
        </>
    );
};

export default StoreRegistration;