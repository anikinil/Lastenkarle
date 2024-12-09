import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';

import './PictureAndDescriptionField.css';

const PictureAndDescriptionField = ({ editable, object, onPictureChange, onDescriptionChange }) => {
    const { t } = useTranslation();

    const [pictureFile, setPictureFile] = useState(object?.image);
    const [description, setDescription] = useState(object?.description);

    function handlePictureFileChange(event) {
        const file = event.target.files[0];
        // THINK if duplication is the best way to handle this
        setPictureFile(file);
        onPictureChange(file);
    }

    const handleImgContainerClick = () => {
        document.getElementById('pictureFileInput').click();
    };

    const handleRemovePictureClick = () => {
        setPictureFile(null);
        onPictureChange(null);
    };

    const handleDescriptionChange = (event) => {
        setDescription(event.target.value);
        onDescriptionChange(event.target.value);
    }

    return (
        <>
            <div className="image-and-description-container">
                <div
                    className={`img-container ${editable ? '' : 'disabled'}`}
                    onClick={handleImgContainerClick}
                >
                    {pictureFile ? (
                        // TODO imlpement proper image handling with respect to backend
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
                    value={object?.description}
                    onChange={handleDescriptionChange}
                    placeholder={editable ? t('write_description') : t('no_description')}
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
