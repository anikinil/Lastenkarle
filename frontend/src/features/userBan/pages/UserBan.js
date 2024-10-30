import React from 'react';
import { useTranslation } from 'react-i18next';

// UserBan component
const UserBan = () => {
    // TODO implement page

    // Hook to use translation functionality
    const { t } = useTranslation();

    return (
        // Render a heading with the translated text for 'user_ban'
        <h1>{t('user_ban')}</h1>
    );
};
  
export default UserBan;