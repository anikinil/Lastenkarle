import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';

import './ImageAndDescriptionField.css';
import { HOST } from '../../../constants/URIs/General';

const ImageAndDescriptionField = ({ editable, object, onImageChange, onDescriptionChange }) => {
    const { t } = useTranslation();

    const [image, setImageFile] = useState(object?.image);
    const [description, setDescription] = useState(object?.description);

    function handleImageFileChange(event) {
        const file = event.target.files[0];
        // THINK if duplication is the best way to handle this
        setImageFile(file);
        onImageChange(file);
    }

    const handleImgContainerClick = () => {
        document.getElementById('imageInput').click();
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
                    {image ? (
                        <img className="img" alt={t('image')} src={HOST + image} />
                    ) : editable ? (
                        <span className="img-container-label">{t('select_an_imagee')}</span>
                    ) : (
                        <span className="img-container-label">{t('no_image')}</span>
                    )}
                </div>

                <input
                    id="imageInput"
                    type="file"
                    title={t('image-selection')}
                    accept="image/*"
                    onChange={handleImageFileChange}
                    style={{ display: 'none' }}
                    disabled={!editable}
                />

                <textarea
                    title={t('write_description')}
                    className="description"
                    value={description}
                    onChange={handleDescriptionChange}
                    placeholder={editable ? t('write_description') : t('no_description')}
                    disabled={!editable}
                ></textarea>
            </div>
        </>
    );
};

export default ImageAndDescriptionField;
