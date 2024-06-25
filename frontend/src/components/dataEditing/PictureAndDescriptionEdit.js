import React, { useState } from "react";
import { useTranslation } from 'react-i18next';

import "./PictureAndDescriptionEdit.css"

const PictureDescriptionEdit = () => {

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
            <div className="image-and-desctiption-container">

                <div className="img-container" type="file" onClick={handleImgContainerClick}>
                    {pictureFile ?
                        <img className="img" alt={t('image')} src={URL.createObjectURL(pictureFile)}></img>
                        :
                        <span className="img-container-label">{t('select_a_picture')}</span>
                    }
                </div>

                <input
                    id="pictureFileInput"
                    type="file"
                    title={t('image-selection')}
                    accept="image/*"
                    onChange={handlePictureFileChange}
                    style={{ display: 'none' }}
                />

                <textarea title={t('write_description')} className="description" placeholder={t('write_description')}></textarea>
            </div>

            <div className="button-container">
                <button type="button" className="button regular" onClick={handleRemovePictureClick}>{t('remove_picture')}</button>
            </div>
        </>
    );
};

export default PictureDescriptionEdit;