import React, { useState } from "react";
import { useTranslation } from 'react-i18next';

import "./AddressEdit.css"

const AddressEdit = () => {

    const { t } = useTranslation();

    // prevents user from switching to new line by hitting [Enter]
    const handleAddressKeyDown = (event) => {
        if (event.key === 'Enter') {
            event.preventDefault();
        }
    };

    return (
        <textarea title={t('enter_address')} className="address" rows="1" onKeyDown={handleAddressKeyDown} placeholder={t('enter_address')}></textarea>
    );
}

export default AddressEdit;