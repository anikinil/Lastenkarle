import React from 'react';
import { useTranslation } from 'react-i18next';



const UserBan = () => {

    const { t } = useTranslation();

    return (
        <h1>{t('user_ban')}</h1>
    );
};
  
export default UserBan;