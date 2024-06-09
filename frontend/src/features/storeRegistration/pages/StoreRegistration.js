import React, { useState } from "react";
import { useTranslation } from 'react-i18next';

import "./StoreRegistration.css"

const StoreRegistration = () => {

    const { t } = useTranslation();

    const [pictureFile, setPictureFile] = useState(null)

    function handlePictureFileChange(event) {
        setPictureFile(event.target.files[0])
    }

    const handleImgContainerClick = () => {
        document.getElementById('pictureFileInput').click();
    };

    const handleRemovePictureClick = () => {
        setPictureFile(null)
    }

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

                <div className="new-store-img-container" type="file" onClick={handleImgContainerClick}>
                    {pictureFile ?
                        <img className="new-store-img" alt={t('store_image')} src={URL.createObjectURL(pictureFile)}></img>
                        :
                        <span>{t('select_a_picture')}</span>
                    }
                </div>

                <input
                    id="pictureFileInput"
                    type="file"
                    accept="image/*"
                    onChange={handlePictureFileChange}
                    style={{ display: 'none' }}
                />

                <textarea title={t('store_description')} className="new-store-description" placeholder={t('store_description')}></textarea>
            </div>

            <div className="button-container">
                <button type="button" className="button regular" onClick={handleRemovePictureClick}>{t('remove_picture')}</button>
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