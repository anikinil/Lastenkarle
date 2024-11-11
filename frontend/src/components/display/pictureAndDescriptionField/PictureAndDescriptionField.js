import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';

import './PictureAndDescriptionField.css';

const PictureAndDescriptionField = ({ editable, object }) => {
    const { t } = useTranslation();

    const [pictureFile, setPictureFile] = useState(object?.image);
    const [description, setDescription] = useState(object?.description);

    function handlePictureFileChange(event) {
        const file = event.target.files[0];
        setPictureFile(file);
    }

    const handleImgContainerClick = () => {
        document.getElementById('pictureFileInput').click();
    };

    const handleRemovePictureClick = () => {
        setPictureFile(null);
    };

    return (
        <>
            <div className="image-and-description-container">
                <div
                    className={`img-container ${editable ? '' : 'disabled'}`}
                    onClick={handleImgContainerClick}
                >
                    {pictureFile ? (
                        <img className="img" alt={t('image')} src={URL.createObjectURL(pictureFile)} />
                    ) : editable ? (
                        <span className="img-container-label">{t('select_a_picture')}</span>
                    ) : (
                        <span className="img-container-label">{t('no_picture')}</span>
                    )}
                </div>

                <input
                    id="pictureFileInput"
                    type="file"
                    title={t('image-selection')}
                    accept="image/*"
                    onChange={handlePictureFileChange}
                    style={{ display: 'none' }}
                    disabled={!editable}
                />

                <textarea
                    title={t('write_description')}
                    className="description"
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                    placeholder={t('write_description')}
                    disabled={!editable}
                ></textarea>
            </div>

            {editable && (
                <div className="button-container">
                    <button
                        type="button"
                        className="button regular"
                        onClick={handleRemovePictureClick}
                    >
                        {t('remove_picture')}
                    </button>
                </div>
            )}
        </>
    );
};

export default PictureAndDescriptionField;
