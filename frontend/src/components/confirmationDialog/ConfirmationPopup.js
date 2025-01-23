import React from 'react';
import { useTranslation } from 'react-i18next';

import './ConfirmationPopup.css'

const ConfirmationPopup = ({ children, onConfirm, onCancel, show }) => {

    const { t } = useTranslation();

    const message = children;

    return (
        <>
            {show ?
                <div className='popup'>
                    <div className='popup-content'>
                        {message}
                        <div className='button-container popup'>
                            <button className='button accent' onClick={onConfirm}>{t('confirm')}</button >
                            <button className='button regular' onClick={onCancel}>{t('cancel')}</button>
                        </div>
                    </div>
                </div > : null
            }
        </>
    );
}

export default ConfirmationPopup;