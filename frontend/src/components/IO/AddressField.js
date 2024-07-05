import React, { useState } from "react";
import { useTranslation } from 'react-i18next';

import "./AddressField.css"

const AddressField = ({ editable, store }) => {

    const { t } = useTranslation();

    const [address, setAddress] = useState(store.address)

    // prevents user from switching to new line by hitting [Enter]
    const handleAddressFieldKeyDown = (event) => {
        if (event.key === 'Enter') {
            event.preventDefault();
        }
    };


    // TODO adjust for address display

    return (
        <textarea
            title={t('enter_address')}
            className="address"
            rows="1"
            value={address}
            onChange={e => setAddress(e.target.value)}
            onKeyDown={handleAddressFieldKeyDown}
            placeholder={t('enter_address')}
            disabled={!editable}>
        </textarea>
    );
}

export default AddressField;