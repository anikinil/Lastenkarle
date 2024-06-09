import React, { useState } from "react";
import { useTranslation } from 'react-i18next';

import "./BikeRegistration.css"

const BikeRegistration = () => {

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

    return (
        <>
            <h1>{t('new_bike')}</h1>

            <div className="new-bike-img-container" type="file" onClick={handleImgContainerClick}>
                {pictureFile ?
                    <img className="new-bike-img" alt={t('bike_image')} src={URL.createObjectURL(pictureFile)}></img>
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

            <textarea title={t('bike_description')} className="new-bike-description"></textarea>

            <div className="button-container">
                <button type="button" className="button picture" onClick={handleRemovePictureClick}>{t('remove_picture')}</button>
            </div>

            <div className="button-container">
                <button type="button" className="button register">{t('register_new_bike')}</button>
            </div>
        </>
    );
};

export default BikeRegistration;